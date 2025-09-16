import os
from flask import Flask
from .api.llm_routes import llm_bp
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializa o aplicativo Flask
app = Flask(__name__)

# Registra o Blueprint para as rotas da LLM
app.register_blueprint(llm_bp, url_prefix='/api/ai')

@app.route('/')
def home():
    return "Serviço de IA está online!", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8003)) # Nova porta para o serviço de IA
    app.run(host='0.0.0.0', port=port)
