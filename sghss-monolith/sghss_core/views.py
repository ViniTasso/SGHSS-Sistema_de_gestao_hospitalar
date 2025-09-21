from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json

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