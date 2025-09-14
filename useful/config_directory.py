"""
USO DO SCRIPT PARA CRIAR DIRETóORIOS

Apos criar a pasta RAIZ, colocar esse codigo dentro da pasta
executar "python3 config_directory.py"
"""

import os
from pathlib import Path

# Define a estrutura de diretórios e arquivos
project_structure = {
    'authentication-service': {
        'app': {
            'api': ['auth_routes.py'],
            'core': ['auth_logic.py'],
            'models': ['user_model.py']
        },
        'files': ['Dockerfile', 'requirements.txt']
    },
    'sghss-monolith': {
        'sghss_core': ['settings.py', 'urls.py'],
        'patients': ['views.py', 'models.py', 'serializers.py'],
        'professionals': ['views.py', 'models.py', 'serializers.py'],
        'appointments': ['views.py', 'models.py', 'serializers.py'],
        'financial': ['views.py', 'models.py'],
        'static': [],
        'files': ['Dockerfile', 'requirements.txt']
    },
    'databases': {
        'postgres': ['init.sql'],
        'mongodb': ['init-mongo.js']
    },
    'root_files': ['docker-compose.yml', '.gitignore', 'README.md']
}

def create_structure(base_path, structure):
    """Cria recursivamente a estrutura de diretórios e arquivos."""
    for name, content in structure.items():
        current_path = base_path / name

        if isinstance(content, dict):
            # É um diretório, então o cria e continua a recursão
            print(f"Criando diretório: {current_path}")
            current_path.mkdir(exist_ok=True)
            create_structure(current_path, content)
        elif isinstance(content, list):
            # É uma lista de arquivos, então os cria
            for file_name in content:
                file_path = base_path / file_name
                print(f"Criando arquivo: {file_path}")
                file_path.touch(exist_ok=True)

# Define o caminho base como o diretório atual
base_directory = Path('..')

# Inicia a criação da estrutura
print("Iniciando a criação da estrutura do projeto SGHSS...")
try:
    # Cria os diretórios e arquivos principais
    create_structure(base_directory, {k: v for k, v in project_structure.items() if k != 'root_files'})

    # Cria os arquivos na raiz do projeto
    for file_name in project_structure['root_files']:
        file_path = base_directory / file_name
        print(f"Criando arquivo na raiz: {file_path}")
        file_path.touch(exist_ok=True)

    print("\nEstrutura do projeto SGHSS criada com sucesso!")

except Exception as e:
    print(f"Ocorreu um erro: {e}")
