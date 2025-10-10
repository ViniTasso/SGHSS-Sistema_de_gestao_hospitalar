# authentication-service/app/core/auth_logic.py

"""
Módulo responsável pela lógica de autenticação do sistema.

Este módulo contém as funções para:
- Criar tokens JWT para usuários autenticados
- Verificar credenciais de usuários no PostgreSQL
- Decodificar e validar tokens JWT
"""

#PRECISA de pip install pymongo mongoengine
#from mongoengine import connect
from .db_connection import get_postgres_conn, set_postgres_conn
import jwt
from datetime import datetime, timedelta
import os
import logging
from passlib.context import CryptContext
import psycopg2 
from psycopg2 import OperationalError, DatabaseError # Importar as exceções do driver


# Constantes de configuração
SECRET_KEY = os.environ.get('SECRET_KEY', 'MINHA_SECRET_KEY_QUE_NO_FIM_NAO_SERVE_PRA_NADA')
ALGORITHM = "HS256"


# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Configuração do contexto de senha para suportar hash do Django
# pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
pwd_context = CryptContext(
    # Adicione 'django_pbkdf2_sha256' à lista de esquemas que ele deve verificar
    schemes=["django_pbkdf2_sha256", "argon2", "bcrypt"], 
    deprecated="auto",
)

def criar_token(user_id):
    """
    Cria um token JWT para o usuário autenticado.
    
    Args:
        user_id: ID do usuário no banco de dados
        
    Returns:
        str: Token JWT codificado
        
    Raises:
        Exception: Se houver erro na geração do token
    """
    # Payload
    payload = {
        'user_id': user_id,
        # Define a expiração para 1 hora a partir de agora
        'exp': datetime.utcnow() + timedelta(hours=1),
        # Define o momento de emissão
        'iat': datetime.utcnow(),
    }
    
    # Codifica o token
    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return token

def verificar_credenciais(username, password):
    """
    Verifica as credenciais do usuário no PostgreSQL.
    
    Busca o usuário pelo username e verifica se a senha fornecida
    corresponde ao hash armazenado no banco de dados.
    
    Args:
        username (str): Nome de usuário
        password (str): Senha em texto plano
        
    Returns:
        tuple: (user_id, error_message)
            - Se sucesso: (user_id, None)
            - Se falha: (None, mensagem_de_erro)
    """

    # Obtém uma nova conexão com o PostgreSQL
    conn = get_postgres_conn()
    if not conn:
        return None, "Serviço de banco de dados indisponível."

    # Busca o user_id e o hash da senha
    sql = "SELECT id, password FROM accounts_user WHERE username = %s;"
    
    try:
        with conn.cursor() as cur:
            # Atenção: O cursor precisa ser fechado/liberado após o uso
            cur.execute(sql, (username,))
            result = cur.fetchone()

        if result:
            user_id, hashed_password = result
            logging.warning(f"DEBUG: Hashed Password Recuperado: '{hashed_password}'")
        
            # Verifica se a senha fornecida corresponde ao hash armazenado
            # O pwd_context usa a biblioteca passlib para validar hashes Django PBKDF2
            if pwd_context.verify(password, hashed_password):
                return user_id, None # Senha correta, retorna o ID
            else:
                return None, "Credenciais invalidas."
        
        return None, "Credenciais inválidas. O hashed_password é "+hashed_password

    # 1. Erros de Banco de Dados: SyntaxError, UndefinedTable, etc.
    # DatabaseError é a base para todos os erros de dados e SQL do psycopg2
    except DatabaseError as e:
        # Loga a exceção e a SQL que causou o problema
        logging.error(f"Erro de Banco de Dados/SQL (DatabaseError): {e}. SQL: {sql}")
        return None, "Erro interno de esquema/consulta no servidor."
        
    # 2. Erros de Operação/Conexão (Timeout, Serviço Indisponível)
    except OperationalError as e:
        # Loga problemas de rede ou acesso ao DB (ex: credenciais erradas no driver)
        logging.error(f"Erro Operacional/Conexão (OperationalError): {e}")
        return None, "Falha na comunicação com o serviço de banco de dados."
    
    # 3. Captura qualquer outra exceção inesperada de Python (segurança)
    except Exception as e:
        # Isso garantirá que nenhum erro cause um 500 genérico no seu framework
        logging.critical(f"Erro Inesperado Não Mapeado durante autenticação: {e}", exc_info=True)
        return None, "Erro interno não tratado. Contate o suporte."

    # 4. Bloco finally para garantir que a conexão seja fechada (BOA PRÁTICA)
    finally:
        if conn:
            # Garante que a conexão sempre seja fechada, mesmo se houver erro
            conn.close()

def decode_token(token):
    """
    Decodifica e valida um token JWT.
    
    Args:
        token (str): Token JWT a ser decodificado
        
    Returns:
        int|None: user_id se o token for válido, None caso contrário
        
    Raises:
        jwt.ExpiredSignatureError: Se o token estiver expirado
        jwt.InvalidTokenError: Se o token for inválido
    """
    try:
        # Se você usar a biblioteca PyJWT, a decodificação já faz a validação
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # A partir daqui, você pode buscar os dados do usuário no seu banco de dados
        # O 'sub' no token geralmente contém o user_id

        """
        DESVANTAGEM DO USO DA DOCKER
            Estava fazendo um teste no código e fiz uma concatenação errada:
                logging.info("O Token é o: "+decoded_token)
            ao invés de fazer corretamente:
                logging.info(f"O Token é o: {decoded_token}")
            Esse código gerava um erro e retornava uma variável null para o user_id
            Por existir o tratamento com except a docker não sinalizava o erro.
            A não ser que eu fizer linha por linha uma delcaração de logging.warning, já que 
            info não é mostrado no log da docker.

            Esse pequeno erro nunca seria visto, como eu já fiz a alteração imaginando que não 
            daria certo, foi a primeira que alterei depois de ver que a lógica estava certa.
            Por uma simples concatenação errada, se eu não lembrasse seria difícil identificar
            o erro, pela abstração que o docker faz.
        """
        #logging.info("O Token é o: {decoded_token}")
        user_id = decoded_token.get('user_id') #decoded.get('sub') # Retorna o user_id

        return user_id
    except jwt.ExpiredSignatureError:
        # Token expirado - relança a exceção para tratamento na rota
        logging.warning("Tentativa de uso de token expirado")
        raise
        
    except jwt.InvalidTokenError:
        # Token inválido - relança a exceção para tratamento na rota
        logging.warning("Tentativa de uso de token inválido")
        raise

    except Exception as e:
        return None
        
# Função para buscar as permissões no PostgreSQL
def get_user_permissions(user_id):
    conn = get_postgres_conn()
    if not conn:
        return []

    # SQL que busca todas as permissões associadas à Role do usuário
    sql = """
    SELECT T2.nome 
    FROM accounts_user AS T1
    JOIN accounts_role AS T2 ON T1.role_id = T2.id
    JOIN accounts_rolepermission AS T3 ON T2.id = T3.role_id
    WHERE T1.id = %s;
    """
    
    try:
        logging.warning("Tentativa de execucao da Query.")
        with conn.cursor() as cur:
            cur.execute(sql, (user_id,))
            # Retorna uma lista de strings de permissões (ex: ['visualizar_prontuario'])
            return [row[0] for row in cur.fetchall()]
    except Exception as e:
        logging.warning("Erro ao buscar permissões: {e}")
        return []
