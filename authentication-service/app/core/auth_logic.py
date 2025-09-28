# authentication-service/app/core/auth_logic.py

#PRECISA de pip install pymongo mongoengine
from mongoengine import connect

def init_db():
    """
    Inicializa a conexão com o banco de dados MongoDB.
    """
    try:
        connect(
            db='auth_db',
            username='user',
            password='password',
            host='db-mongodb',  # Nome do serviço no docker-compose.yml
            port=27017,
            alias='default'
        )
        print("Conexão com o MongoDB estabelecida com sucesso!")
    except Exception as e:
        print(f"Errou ao conectar ao MongoDB: {e}")
        # Considerar encerrar a aplicação em caso de falha crítica

# Chame a função de inicialização na sua aplicação principal
# init_db()
