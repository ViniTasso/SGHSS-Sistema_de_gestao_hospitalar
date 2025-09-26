from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from django.db import transaction
from accounts.models import User, Role
from patients.models import Patient
import os
#Middleware reutilizado para segurança do endpoint - Funcao auxiliar
from .decorators import jwt_required

AUTH_SERVICE_URL = 'http://authentication-service:8001/api/auth/login'

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            # Recebe os dados do frontend
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            # Envia a requisição para o microsserviço de autenticação
            response = requests.post(AUTH_SERVICE_URL, json={'username': username, 'password': password})
            
            # Retorna a resposta do microsserviço para o frontend
            if response.status_code == 200:
                return JsonResponse(response.json(), status=200)
            else:
                return JsonResponse(response.json(), status=response.status_code)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    return JsonResponse({'error': 'Método não permitido'}, status=405)

@csrf_exempt
@transaction.atomic
def register_patient_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            nome_completo = data.get('nome_completo')
            cpf = data.get('cpf')

            try:
                #Foi preciso utilizar o .first(). Erro ao procurar 'paciente', provavel duplicação, e get só aceitava 1 campo.
                patient_role = Role.objects.filter(nome='paciente').first() 
            except Role.DoesNotExist:
                return JsonResponse({'error': 'Role "paciente" nao encontrada'}, status=500)

            """
                Ao inserir o Paciente, estava dando esse erro:
                    {"error": "null value in column \"first_name\" of relation \"accounts_user\" violates not-null constraint\nDETAIL:  Failing row contains (pbkdf2_sha256$600000$jniAncZqxlqw8wVOulRItD$Nv6PYSbw/R99OmM77PNo..., null, f, joao.silva, null, null, null, f, t, null, null, f5b5b505-b445-4d37-90e6-928e7f9b1cab).\n"}
                Significa que o projeto ta usando o defalt do AbstractUser.
                    Mesmo que não está explicito no código o first_name ele pega do models.

                Solução
                    1. Modificar CustomUserManager e deixar explicito o uso do first e last_name
                    2. permitir acesso =null para first e last_name
                    3. Colocar "" para a variável.

                Selecionei vazio momentaneamente para rodar o código.
            """
            user = User.objects.create_user(
                username=username, 
                password=password
                #first_name='',
                #last_name='', 
                #email=''
                )
            user.role = patient_role
            user.save()

            patient = Patient.objects.create(
                user=user,
                nome_completo=nome_completo,
                cpf=cpf
            )

            return JsonResponse({
                'message': 'Paciente cadastrado com sucesso!',
                'patient_id': patient.user.id
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Método não permitido'}, status=405)

@csrf_exempt
@jwt_required # Usa o decorator para proteger a rota
def get_patient_record_view(request, patient_id):
    # O user_data já foi injetado pelo decorator
    user_data = request.user_data

    # A partir daqui, você pode usar os dados do usuário para verificar permissões
    # Por exemplo, verificar se o usuário logado tem a permissão 'visualizar_prontuario'
    permissions = user_data.get('permissions', [])
    if 'visualizar_prontuario' not in permissions:
        return JsonResponse({'error': 'Permissão negada'}, status=403)

    # Se a permissão existir, a lógica de negócio continua
    return JsonResponse({'message': f'Acesso concedido ao prontuário do paciente {patient_id}'}, status=200)