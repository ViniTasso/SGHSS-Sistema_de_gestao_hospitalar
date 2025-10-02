from flask import Blueprint, request, jsonify
# from ..core.auth_logic import ... (vamos adicionar isso depois)
import jwt #somente se for necessário
import os
from datetime import timedelta, datetime
import logging

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

    # A lógica de autenticação e geração de token viria aqui
    # Por enquanto, é apenas um placeholder
    if username == 'test' and password == 'test':
        # Gera e retorna um JWT
        #token = "seu-jwt-aqui"
        token = criar_token(1)
        return jsonify({"token": token}), 200

    return jsonify({"message": "Credenciais inválidas"}), 401

#@auth_bp.route('/login/', methods=['POST'])
#def login():

def criar_token(user_id):
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

@auth_bp.route('/validate', methods=['GET'])
def validate():
    # Lógica para validar o token JWT viria aqui - O retorno era Bearer TOKEN - não aceitava por estar com erro
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Token não fornecido ou formato inválido'}), 401
    
    token = auth_header.split(' ')[1]
    
    try:
        # A lógica de validação do token e decodificação
        # O 'verify' abaixo deve ser implementado por você, mas aqui está um exemplo
        # Se você usar a biblioteca PyJWT, a decodificação já faz a validação
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        
        # A partir daqui, você pode buscar os dados do usuário no seu banco de dados
        # O 'sub' no token geralmente contém o user_id
        logging.info(decoded_token)
        user_id = decoded_token.get('user_id')
        
        # Crie a lógica para obter os dados do usuário, permissões, etc.
        # Exemplo: user_data = db.get_user(user_id)
        
        # Retorne os dados para o monolito
        return jsonify({
            'user_id': user_id,
            'permissions': ['visualizar_prontuario'] # Exemplo de permissões
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