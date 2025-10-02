from functools import wraps
from django.http import JsonResponse
import requests
import os

AUTH_SERVICE_VALIDATE_URL = os.environ.get('AUTH_SERVICE_VALIDATE_URL', 'http://authentication-service:8001/api/auth/validate')

def jwt_required(f):
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        # 1. Tenta obter o token do cabeçalho
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({'error': 'Token não fornecido ou formato inválido'}, status=401)
        
        token = auth_header.split(' ')[1]
        
        # 2. Envia o token para o microsserviço de autenticação para validação
        try:
            print("2. Envia o token para o microsserviço de autenticação para validação")
            response = requests.get(
                AUTH_SERVICE_VALIDATE_URL,
                headers={'Authorization': f'Bearer {token}'}
            )
            
            if response.status_code == 200:
                # 3. Se o token for válido, adiciona os dados do usuário à requisição e continua
                request.user_data = response.json()
                return f(request, *args, **kwargs)
            else:
                return JsonResponse(response.json(), status=401)
        except requests.exceptions.RequestException:
            return JsonResponse({'error': 'Não foi possível conectar ao serviço de autenticação'}, status=503)

    return decorated_function