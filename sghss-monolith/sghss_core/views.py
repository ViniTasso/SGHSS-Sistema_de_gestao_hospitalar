from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from django.db import transaction
from accounts_1.models import User, Role
from patients.models import Patient

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
                patient_role = Role.objects.get(nome='paciente')
            except Role.DoesNotExist:
                return JsonResponse({'error': 'Role "paciente" não encontrada'}, status=500)

            user = User.objects.create_user(username=username, password=password)
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