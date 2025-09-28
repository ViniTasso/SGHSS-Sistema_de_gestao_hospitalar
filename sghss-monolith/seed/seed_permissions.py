
"""
    Como Usar o Script com Docker
        1. Garanta que as migrações foram aplicadas: Execute docker compose run --rm sghss-monolith python manage.py migrate para criar as tabelas Role e Permission.
        2. Execute o script de seed: O comando docker compose run é perfeito para isso, pois ele irá criar um contêiner temporário, executar o script e depois removê-lo.
            docker compose run --rm sghss-monolith python seed/seed_permissions.py

    Explicação:
        O get_or_create() é uma função do Django que cria um objeto se ele não existir, o que torna o script seguro para ser executado várias vezes.
 

    Se preferir escrever direto no SHELL
    docker compose run --rm sghss-monolith python manage.py shell

    >>> from accounts.models import Role, Permission, RolePermission
    >>> visualizar_prontuario = Permission.objects.create(nome_acao='visualizar_prontuario', descricao='Pode visualizar prontuários de pacientes.')
    >>> paciente_role = Role.objects.get(nome='paciente')
    >>> RolePermission.objects.create(role=paciente_role, permission=visualizar_prontuario)
    >>> exit()
"""

#!/usr/bin/env python
import os
import django
import sys
from pathlib import Path

# --- 1. Calcular o Caminho da Pasta Raiz ---
# Calcula o caminho do diretório atual (onde seed.py está)
CURRENT_DIR = Path(__file__).resolve().parent

# Sobe um nível para encontrar a pasta raiz 'app/'
# Se 'seed' está em 'app/seed/', este será 'app/'
PROJECT_ROOT = CURRENT_DIR.parent

# --- 2. Adicionar a Pasta Raiz ao Caminho de Importação do Python ---
# Isso permite que o Python encontre 'sghss_core'
# Antes, tentei acessar com uso de '/' ./sghss_core.settings, causa erro TypeError
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# --- 3. Definir a Variável de Ambiente (Referência Python) ---
# O Django agora pode importar 'sghss_core.settings' porque 'app/' está no sys.path
# NUNCA use barras (./) aqui, apenas a referência de importação do Python.
# Garante que o ambiente do Django seja configurado
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sghss_core.settings')
django.setup()

from accounts.models import Role, Permission, RolePermission
from django.db import transaction

def seed_permissions():
    """
    Cria as roles e permissions necessárias para o projeto.

        O with transaction.atomic(): Ele garante que todas as etapas dentro do bloco sejam concluídas com sucesso. Se alguma coisa der errado em qualquer uma das etapas, o Django automaticamente desfaz todas as alterações que foram feitas no banco de dados.
    """
    print("Iniciando a criação das roles e permissões...")

    try:
        with transaction.atomic():
            # Criação das Roles
            paciente_role, created = Role.objects.get_or_create(nome='paciente')
            profissional_role, _ = Role.objects.get_or_create(nome='profissional')
            admin_role, _ = Role.objects.get_or_create(nome='administrador')

            if created:
                print(f"Role '{paciente_role.nome}' criada com sucesso.")
            
            # Criação da Permissão
            visualizar_prontuario, created = Permission.objects.get_or_create(
                nome_acao='visualizar_prontuario',
                defaults={'descricao': 'Pode visualizar prontuários de pacientes.'}
            )

            if created:
                print(f"Permissão '{visualizar_prontuario.nome_acao}' criada com sucesso.")

            # Associação da Permissão com a Role
            RolePermission.objects.get_or_create(
                role=paciente_role,
                permission=visualizar_prontuario
            )
            print("Permissões associadas com sucesso.")

    except Exception as e:
        print(f"Erro ao criar permissões: {e}")
        sys.exit(1)

if __name__ == "__main__":
    seed_permissions()