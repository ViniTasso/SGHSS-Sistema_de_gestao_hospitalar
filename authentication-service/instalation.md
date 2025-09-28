## Pymongo
Eu só consegui instalar o pip install pymongo mongoengine
depois que criou o espaco virtual venv

#Criar um ambiente virtual sudo apt install python3.12-venv
#python3 -m venv venv #para criar um ambiente virtual
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install Flask PyMongo mongoengine Flask-PyMongo PyJWT python-dotenv


## Passo 1: Configuração Inicial do Projeto

Primeiro, navegue até a pasta authentication-service no seu terminal e instale as bibliotecas necessárias para o nosso projeto Flask. Crie um ambiente virtual (venv) para isolar as dependências.
Bash

cd authentication-service/
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install Flask PyMongo Flask-PyMongo PyJWT python-dotenv

    Flask: O microframework web que é usado.

    PyMongo: O driver oficial para conectar ao MongoDB.

    PyJWT: Biblioteca para criar e validar JSON Web Tokens (JWT).

    python-dotenv: Para carregar variáveis de ambiente de forma segura.

## Passo 2: O Arquivo Principal (app.py)

Vamos criar o arquivo principal da nossa aplicação Flask dentro da pasta app/. Este arquivo será o ponto de entrada do microsserviço.

authentication-service/app/app.py
Python

import os
from flask import Flask
from .api.auth_routes import auth_bp
from .core.db_connection import init_db

Inicializa o aplicativo Flask
app = Flask(__name__)

 Carrega as variáveis de ambiente (se necessário)
 app.config.from_pyfile('.env') 

 Inicializa a conexão com o banco de dados
init_db(app)

 Registra o Blueprint para as rotas de autenticação
app.register_blueprint(auth_bp, url_prefix='/api/auth')

@app.route('/')
def home():
    return "Serviço de Autenticação está online!", 200

if __name__ == '__main__':
    # Obtém a porta da variável de ambiente ou usa a padrão 8001
    port = int(os.environ.get('PORT', 8001))
    app.run(host='0.0.0.0', port=port)

## Passo 3: Conexão com o Banco de Dados

Crie o arquivo db_connection.py dentro da pasta app/core/. Ele irá gerenciar a conexão com o MongoDB.

authentication-service/app/core/db_connection.py
Python

from pymongo import MongoClient

mongo_client = None

def init_db(app):
    global mongo_client
    try:
        # Pega as variáveis de ambiente do Flask
        mongo_url = app.config.get('MONGO_URL', 'mongodb://user:password@db-mongodb:27017/auth_db')
        mongo_client = MongoClient(mongo_url)
        
        # Teste de conexão
        mongo_client.admin.command('ping')
        print("Conexão com o MongoDB estabelecida com sucesso!")
        
    except Exception as e:
        print(f"Erro ao conectar ao MongoDB: {e}")
        mongo_client = None # Garante que o cliente é None em caso de falha

def get_db():
    return mongo_client.auth_db

## Passo 4: Rotas da API de Autenticação

Crie o arquivo auth_routes.py dentro da pasta app/api/. Este arquivo conterá a lógica para os endpoints de login e validação.

authentication-service/app/api/auth_routes.py
Python

from flask import Blueprint, request, jsonify
 from ..core.auth_logic import ... (vamos adicionar isso depois)

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # A lógica de autenticação e geração de token viria aqui
    # Por enquanto, é apenas um placeholder
    if username == 'test' and password == 'test':
        # Gera e retorna um JWT
        token = "seu-jwt-aqui" 
        return jsonify({"token": token}), 200
    
    return jsonify({"message": "Credenciais inválidas"}), 401

@auth_bp.route('/validate', methods=['GET'])
def validate():
    # Lógica para validar o token JWT viria aqui
    token = request.headers.get('Authorization')
    if token == "seu-jwt-aqui":
        return jsonify({"message": "Token válido", "user_id": "12345"}), 200
    
    return jsonify({"message": "Token inválido"}), 401

Com este código, você tem a estrutura básica do nosso microsserviço de autenticação, pronta para ser executada e testada no Docker.

## CONFIGURAÇÃO DO DOCKER

# Considere os seguintes pontos para criar um Dockerfile corretamente:

    Tamanho da Imagem: Use imagens base menores (python:3.9-slim) para reduzir o tempo de download e o consumo de armazenamento.

    Camadas Otimizadas: A ordem dos comandos no Dockerfile importa. A instrução COPY requirements.txt seguida de RUN pip install deve vir antes do COPY . .. Isso faz com que o Docker não reinstale as dependências toda vez que você fizer uma pequena alteração no seu código.

    Variáveis de Ambiente: Não adicione segredos (como senhas ou chaves de API) diretamente no Dockerfile. Eles devem ser passados de forma segura através de variáveis de ambiente no docker-compose.yml (usando env_file).

    Separar Desenvolvimento de Produção: O comando CMD acima é ideal para desenvolvimento. Em produção, você usaria um servidor mais robusto e seguro, como o Gunicorn ou Waitress, ao invés do servidor de desenvolvimento do Flask.

    Isolamento de Redes: A sua aplicação deve se conectar a outros serviços (como o MongoDB) usando o nome do serviço definido no docker-compose.yml (db-mongodb). O Dockerfile deve ser agnóstico quanto à infraestrutura externa.

# O que Cada porta significa? Ports: 8002:8001
    docker-compose.yml 
        consta como ports: 8002:8001

    dockerfile
        consta EXPOSE 8001


    EXPOSE no Dockerfile informa ao Docker qual porta o container está escutando internamente. É uma documentação da porta do aplicativo. Ele não a torna acessível do lado de fora.

    ports no docker-compose.yml faz o mapeamento real entre o seu computador (o host) e o container. Ele torna a porta do container acessível.

    A sintaxe ports: - "8002:8001" significa:

        8002: A porta no seu computador (localhost) que você usa para acessar o serviço.

        8001: A porta interna do container, onde a sua aplicação Flask está rodando.

    O que precisa ser igual

        A porta no EXPOSE do seu Dockerfile precisa ser igual à segunda porta no seu docker-compose.yml (:8001). Isso garante que a porta interna que você está expondo no container seja a mesma que você está mapeando.

        A porta que você acessa pelo navegador ou curl é a primeira no docker-compose.yml (8002).