#irá gerenciar a conexão com o MongoDB.
from pymongo import MongoClient

mongo_client = None

def init_db(app):
    global mongo_client
    try:
        # Pega as variáveis de ambiente do Flask
        mongo_url = app.config.get('MONGO_URL', 'mongodb://user:password@db-mongodb:27017/auth_db')
        mongo_client = MongoClient(mongo_url)

        # Especificar a base de autenticação
        mongo_client = MongoClient(
            host='db-mongodb',
            port='27017',
            username='user',
            password='password',
            authSource='admin' #linha adicionada por erro de authenticação no auth_db

        )
        # Teste de conexão
        mongo_client.admin.command('ping')
        print("Conexão com o MongoDB estabelecida com sucesso!")

    except Exception as e:
        print(f"Erro ao conectar ao MongoDB: {e}")
        mongo_client = None # Garante que o cliente é None em caso de falha

def get_db():
    #return mongo_client.auth_db
    return mongo_client.get_database('auth_db')
