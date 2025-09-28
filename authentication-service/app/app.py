import os
from flask import Flask
from .api.auth_routes import auth_bp
from .core.db_connection import init_db
import logging

# Inicializa o aplicativo Flask
app = Flask(__name__)

# Carrega as variáveis de ambiente (se necessário)
# app.config.from_pyfile('.env')

# Inicializa a conexão com o banco de dados
init_db(app)

# Registra o Blueprint para as rotas de autenticação
app.register_blueprint(auth_bp, url_prefix='/api/auth')

@app.route('/')
def home():
    return "Serviço de Autenticação está online!", 200

# Configura o logger para mostrar logs de WARNING para cima
logging.basicConfig(level=logging.WARNING)

if __name__ == '__main__':
    # Obtém a porta da variável de ambiente ou usa a padrão 8001
    port = int(os.environ.get('PORT', 8002))
    try:
        logging.info(f"Tentando iniciar API na porta: {port}")
        app.run(host='0.0.0.0', port=port)
    except Exception as e:
        # Se falhar, registra a exceção detalhada no log
        logging.critical(f"Falha CRÍTICA ao iniciar o servidor: {e}", exc_info=True)