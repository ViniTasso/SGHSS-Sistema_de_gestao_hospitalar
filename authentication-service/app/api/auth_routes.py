from flask import Blueprint, request, jsonify
# from ..core.auth_logic import ... (vamos adicionar isso depois)
import jwt #somente se for necessário
import os
from datetime import timedelta, datetime
import logging
from ..core.auth_logic import criar_token, verificar_credenciais, decode_token, get_user_permissions

# Definir a chave secreta do JWT SECRET_KEY = 'MINHA_SECRET_KEY_QUE_NO_FIM_NAO_SERVE_PRA_NADA'
SECRET_KEY = os.environ.get('SECRET_KEY', 'MINHA_SECRET_KEY_QUE_NO_FIM_NAO_SERVE_PRA_NADA')
ALGORITHM = "HS256"

auth_bp = Blueprint('auth_bp', __name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Verifica credenciais no PostgreSQL
    user_id, error_message = verificar_credenciais(username, password)

    if user_id:
        # Se as credenciais estiverem corretas, cria o token
        logging.warning(f"DEBUG: User ID Recuperado: '{user_id}'")
        token = criar_token(user_id) 
        return jsonify({"token": token}), 200
    else:
        # Retorna a mensagem de erro da função verificar_credenciais
        return jsonify({"message": error_message}), 401

@auth_bp.route('/validate', methods=['GET'])
def validate():
    # Lógica para validar o token JWT viria aqui - O retorno era Bearer TOKEN - não aceitava por estar com erro
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Token não fornecido ou formato inválido'}), 401
    
    token = auth_header.split(' ')[1]
    
    try:
        
        # Crie a lógica para obter os dados do usuário, permissões, etc.
        # Exemplo: user_data = db.get_user(user_id)
        user_id = decode_token(token)

        permissions = get_user_permissions(user_id)

        # Retorne os dados para o monolito
        return jsonify({
            'user_id': user_id,
            'permissions': permissions
        }), 200

    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expirado'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Token inválido'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    """
    if token == "[seu-jwt-aqui]":
        return jsonify({"message": "Token válido", "user_id": "12345"+token}), 200
    
    return jsonify({'error': 'Token fornecido não tem validade'}), 401
    #return jsonify({"message": "Token inválido"}), 401

    
    #ESSE É O INICIO DA NOVA AUTHENTICAÇÃO

    #PRECISA ADEQUAR O CÓDIGO PARA CONSEGUIR USAR TOKENS VERDADEIROS

    """

# @auth_bp.rout('/get_users', methods['POST'])
# def get_users():
#     conn = get_postgres_conn()
#     if not conn:
#         return None, "Serviço de banco de dados indisponível."

#     # Busca o user_id e o hash da senha
#     sql = "SELECT * FROM accounts_user"
    
#     try:
#         with conn.cursor() as cur:
#             # Atenção: O cursor precisa ser fechado/liberado após o uso
#             cur.execute(sql)
#             result = cur.fetchone()

#         if result:
#             return jsonify({"usuarios":  result}),200
        
#         return jsonify({"error":  "Nao existe usuario cadastrado"}),200

#     except Exception as e:
#         print(f"Erro na consulta SQL: {e}")
#         # Retorne um erro genérico de credenciais para evitar vazamento de informações
#         return None, "Credenciais inválidas."