#irá gerenciar a conexão com o MongoDB.
from pymongo import MongoClient
import psycopg2
import os

mongo_client = None
postgres_conn = None

# URL de conexão do PostgreSQL (POSTGRES_URL)
POSTGRES_URL = os.environ.get('POSTGRES_DB_URL', 'postgresql://user:password@db-postgres:5432/sghss_db')


def init_db(app):
    """ Inicializa as conexões com MongoDB e PostgreSQL. """
    global mongo_client, postgres_conn
    
    # 1. Conexão com MongoDB (para Logs)
    try:
        # # Pega as variáveis de ambiente do Flask
        # mongo_url = app.config.get('MONGO_URL', 'mongodb://user:password@db-mongodb:27017/auth_db')
        # mongo_client = MongoClient(mongo_url)
        mongo_client = MongoClient(
            host='db-mongodb', port=27017, username='user', password='password', authSource='admin'
        )
        mongo_client.admin.command('ping')
        print("Conexão com MongoDB estabelecida.")
    except Exception as e:
        print(f"ERRO CRÍTICO: Falha na conexão com MongoDB: {e}")
        mongo_client = None # Garante que o cliente é None em caso de falha

    # 2. Conexão com PostgreSQL (para Credenciais)
    try:
        # Use o POSTGRES_URL definido acima
        postgres_conn = psycopg2.connect(POSTGRES_URL)
        print("Conexão com PostgreSQL estabelecida.")
    except Exception as e:
        print(f"ERRO CRÍTICO: Falha na conexão com PostgreSQL: {e}")
        postgres_conn = None


def get_postgres_conn():
    """ Retorna o objeto de conexão com o PostgreSQL. """
    """Tenta estabelecer e retornar uma nova conexão com o PostgreSQL."""
    if not POSTGRES_URL:
        # Se a variável de ambiente não estiver definida
        print("ERRO: POSTGRES_URL não está configurada.")
        return None
    try:
        # 🚨 Retorna uma nova conexão a cada chamada 🚨
        conn = psycopg2.connect(POSTGRES_URL)
        return conn
    except Exception as e:
        # Loga falhas críticas de conexão (ex: DB fora do ar)
        print(f"ERRO CRÍTICO: Falha ao criar conexão com PostgreSQL: {e}")
        return None

def get_mongo_db():
    """ Retorna a base de dados auth_db (para Logs). """
    return mongo_client.get_database('auth_db')

def set_postgres_conn():
    try:
        # Use o POSTGRES_URL definido acima
        postgres_conn = psycopg2.connect(POSTGRES_URL)
        print("Conexão com PostgreSQL estabelecida.")
    except Exception as e:
        print(f"ERRO CRÍTICO: Falha na conexão com PostgreSQL: {e}")
        postgres_conn = None