
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

        O with transaction.atomic(): 
            Ele garante que todas as etapas dentro do bloco sejam concluídas com sucesso. 
            Se alguma coisa der errado em qualquer uma das etapas, o Django automaticamente desfaz 
            todas as alterações que foram feitas no banco de dados.
    """
    print("Iniciando a criação das roles e permissões...")

    try:
        with transaction.atomic():
            # Criação das Roles
            paciente_role, created = Role.objects.get_or_create(nome='paciente')
            medico_role, _ = Role.objects.get_or_create(nome='medico')
            enfermeiro_role, _ = Role.objects.get_or_create(nome='enfermeiro')
            enfermeiro_tecnico_role, _ = Role.objects.get_or_create(nome='enfermeiro_tecnico')
            admin_role, _ = Role.objects.get_or_create(nome='administrador')

            if created:
                print(f"Role '{paciente_role.nome}' criada com sucesso.")
            
            # Criação da Permissão
            visualizar_prontuario, created = Permission.objects.get_or_create(
                nome_acao='visualizar_prontuario',
                defaults={'descricao': 'Pode visualizar prontuários de pacientes.'}
            )
            agendar_consulta, _ = Permission.objects.get_or_create(
                nome_acao='agendar_consulta',
                defaults={'descricao': 'Pode agendar consultas.'}
            )
            telemedicina, _ = Permission.objects.get_or_create(
                nome_acao='telemedicina',
                defaults={'descricao': 'Pode realizar chamadas de telemedicina.'}
            )
            criar_prescricao, _ = Permission.objects.get_or_create(
                nome_acao='criar_prescricao',
                defaults={'descricao': 'Pode criar priscrições para pacientes.'}
            )
            solicitar_exames, _ = Permission.objects.get_or_create(
                nome_acao='solicitar_exames',
                defaults={'descricao': 'Pode criar solicitação para exames.'}
            )
            visualizar_consultas, _ = Permission.objects.get_or_create(
                nome_acao='visualizar_consultas',
                defaults={'descricao': 'Pode visualizar as consultas.'}
            )
            gerenciar_leitos, _ = Permission.objects.get_or_create(
                nome_acao='gerenciar_leitos',
                defaults={'descricao': 'Pode realizar a gerência de leitos.'}
            )
            gerenciar_suprimentos, _ = Permission.objects.get_or_create(
                nome_acao='gerenciar_suprimentos',
                defaults={'descricao': 'Pode realizar a gerência de suprimentos.'}
            )
            dashboard, _ = Permission.objects.get_or_create(
                nome_acao='dashboard',
                defaults={'descricao': 'Pode acessar página de dashboard.'}
            )
            prontuarios, _ = Permission.objects.get_or_create(
                nome_acao='prontuarios',
                defaults={'descricao': 'Pode acessar página de prontuarios.'}
            )
            prescricoes, _ = Permission.objects.get_or_create(
                nome_acao='prescricoes',
                defaults={'descricao': 'Pode acessar página de prescricoes.'}
            )
            leitos, _ = Permission.objects.get_or_create(
                nome_acao='leitos',
                defaults={'descricao': 'Pode acessar página de leitos.'}
            )
            if created:
                print(f"Permissão '{visualizar_prontuario.nome_acao}' criada com sucesso.")

            # Associação da Permissão com a Role
            RolePermission.objects.get_or_create(
                role=enfermeiro_role,
                permission=leitos
            )
            RolePermission.objects.get_or_create(
                role=enfermeiro_role,
                permission=gerenciar_suprimentos
            )
            RolePermission.objects.get_or_create(
                role=enfermeiro_role,
                permission=gerenciar_leitos
            )
            RolePermission.objects.get_or_create(
                role=medico_role,
                permission=prescricoes
            )
            RolePermission.objects.get_or_create(
                role=enfermeiro_role,
                permission=prontuarios
            )
            RolePermission.objects.get_or_create(
                role=paciente_role,
                permission=visualizar_consultas
            )
            RolePermission.objects.get_or_create(
                role=enfermeiro_role,
                permission=visualizar_consultas
            )
            RolePermission.objects.get_or_create(
                role=medico_role,
                permission=solicitar_exames
            )
            RolePermission.objects.get_or_create(
                role=medico_role,
                permission=visualizar_prontuario
            )
            RolePermission.objects.get_or_create(
                role=paciente_role,
                permission=visualizar_prontuario
            )
            RolePermission.objects.get_or_create(
                role=enfermeiro_role,
                permission=visualizar_prontuario
            )
            RolePermission.objects.get_or_create(
                role=paciente_role,
                permission=dashboard
            )
            RolePermission.objects.get_or_create(
                role=enfermeiro_tecnico_role,
                permission=dashboard
            )
            RolePermission.objects.get_or_create(
                role=enfermeiro_role,
                permission=dashboard
            )
            RolePermission.objects.get_or_create(
                role=medico_role,
                permission=dashboard
            )
            print("Permissões associadas com sucesso.")

    except Exception as e:
        print(f"Erro ao criar permissões: {e}")
        sys.exit(1)

def cleanup_permissions():
    """
    Exclui todos os dados relacionados a Roles, Permissions e associações,
    garantindo que o próximo seed comece do zero.
    """
    print("Iniciando a exclusão de todas as Roles, Permissões e associações...")

    try:
        with transaction.atomic():
            # 1. Excluir Associações (Foreign Keys)
            # É crucial remover as associações (RolePermission) primeiro, 
            # pois elas têm chaves estrangeiras para Role e Permission.
            deleted_rp_count, _ = RolePermission.objects.all().delete()
            print(f"-> Associações RolePermission excluídas: {deleted_rp_count}")
            
            # 2. Excluir Roles
            deleted_role_count, _ = Role.objects.all().delete()
            print(f"-> Roles excluídas: {deleted_role_count}")

            # 3. Excluir Permissões
            deleted_perm_count, _ = Permission.objects.all().delete()
            print(f"-> Permissões excluídas: {deleted_perm_count}")

            print("Limpeza de permissões concluída com sucesso. O banco está pronto para um novo SEED.")

    except Exception as e:
        print(f"Erro ao excluir permissões e roles: {e}")
        sys.exit(1)

if __name__ == "__main__":
    cleanup_permissions()
    seed_permissions()