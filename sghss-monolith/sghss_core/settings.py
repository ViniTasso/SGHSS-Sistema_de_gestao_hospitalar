# sghss_monolith/sghss_core/settings.py

"""
Configurações do Django para o SGHSS
Incluindo suporte CORS para comunicação com frontend
"""

#É a configuração ORM
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Apps locais
    'accounts',
    'patients',
    'sghss_core',
    
    # Third party apps - Antes do POST navegadores pede preflight
    'corsheaders',  # IMPORTANTE: Para permitir o serviço responder as requisições OPTIONS ("preflight")
    #'rest_framework',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # IMPORTANTE: Adicione ANTES do CommonMiddleware precisa vir antes para gerar respostas
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

#ALLOWED_HOSTS = ['localhost', '127.0.0.1'] #Para resolver o erro de rodar em produção -->>> sghss-monolith          | CommandError: You must set settings.ALLOWED_HOSTS if DEBUG is False. sghss-monolith exited with code 1 
#também permitir o nome do container
ALLOWED_HOSTS = os.environ.get(
    'ALLOWED_HOSTS', 
    'localhost,127.0.0.1,sghss-monolith'
).split(',')

AUTH_USER_MODEL = 'accounts.User' #O AUTH_USER_MODEL é crucial para dizer ao Django que a sua classe User personalizada é a que deve ser usada para o sistema de autenticação.
ROOT_URLCONF = 'sghss_core.urls'
# SECRET_KEY = 'MINHA_SECRET_KEY_QUE_NO_FIM_NAO_SERVE_PRA_NADA'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-this-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

ROOT_URLCONF = 'sghss_core.urls'

#Após inserir essa configuração, o projeto começou pedir o arquivo wsgi.py
WSGI_APPLICATION = 'sghss_core.wsgi.application'




# ==================== NOVAS CONFIGURAÇÕES ====================



# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
#auth_logic - POSTGRES_URL = os.environ.get('POSTGRES_DB_URL', 'postgresql://user:password@db-postgres:5432/sghss_db')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'sghss_db'),
        'USER': os.environ.get('POSTGRES_USER', 'user'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'password'),
        'HOST': os.environ.get('POSTGRES_HOST', 'db-postgres'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==================== CONFIGURAÇÕES DE AUTENTICAÇÃO ====================

# URL do serviço de autenticação para validação de tokens
AUTH_SERVICE_VALIDATE_URL = os.environ.get(
    'AUTH_SERVICE_VALIDATE_URL',
    'http://authentication-service:8060/api/auth/validate'
)

# Modelo de usuário customizado (se aplicável)
AUTH_USER_MODEL = 'accounts.User'

# ==================== CONFIGURAÇÕES CORS ====================

# Permitir credenciais (cookies, headers de autorização)
CORS_ALLOW_CREDENTIALS = True

# ⭐ OPÇÃO 1: Permitir origens específicas (RECOMENDADO PARA PRODUÇÃO)
#antigo CORS_ALLOWED_ORIGINS = [    "http://localhost:8080", "http://127.0.0.1:8080",    "http://localhost:3000", ] # Se usar React/Vue em desenvolvimento
#Origens permitidas - frontend pode estar em diferentes portas
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = os.environ.get(
    'CORS_ALLOWED_ORIGINS',
    'http://localhost:8000,http://127.0.0.1:8050,http://localhost:3000, http://0.0.0.0:8000'
).split(',')

# ⭐ OPÇÃO 2: Permitir TODAS as origens (APENAS PARA DESENVOLVIMENTO)
# ATENÇÃO: NUNCA use isso em produção!
# CORS_ALLOW_ALL_ORIGINS = True  # Descomente apenas para desenvolvimento

# Headers permitidos nas requisições
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Métodos HTTP permitidos
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# ==================== CONFIGURAÇÕES CSRF ====================

# Isentar as rotas de API da verificação CSRF (pois usamos JWT)
# ATENÇÃO: Apenas para APIs que usam token JWT
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

# Se você está usando apenas API com JWT, pode desabilitar CSRF para endpoints específicos
# usando o decorator @csrf_exempt nas views

# ==================== CONFIGURAÇÕES DE SEGURANÇA ====================

# Configurações de segurança para produção
if not DEBUG:
    # HTTPS settings
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    
    # HSTS settings
    SECURE_HSTS_SECONDS = 31536000  # 1 ano
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Atualizar CORS_ALLOWED_ORIGINS para URLs de produção
    CORS_ALLOWED_ORIGINS = [
        "https://sghss.com",
        "https://www.sghss.com",
    ]
    
    CSRF_TRUSTED_ORIGINS = [
        "https://sghss.com",
        "https://www.sghss.com",
    ]


# ==================== CRIAR DIRETÓRIO DE LOGS ====================
# Cria o diretório de logs se não existir
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)
    print(f"✅ Diretório de logs criado: {LOGS_DIR}")

# ==================== LOGGING ====================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'sghss_core': {
            'handlers': ['console', 'file'],
            #'level': 'DEBUG' if DEBUG else 'INFO',
            'level': 'DEBUG' if os.getenv('DEBUG', 'False') == 'True' else 'INFO',
            'propagate': False,
        },
    },
}

# ==================== REST FRAMEWORK ====================

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'rest_framework.authentication.SessionAuthentication',
#     ],
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.IsAuthenticated',
#     ],
#     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
#     'PAGE_SIZE': 20,
# }

# ==================== CONFIGURAÇÕES ADICIONAIS ====================

# Tamanho máximo de upload de arquivos (em bytes)
# 10MB para imagens de exames
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760

# Tempo de expiração da sessão (em segundos)
SESSION_COOKIE_AGE = 3600  # 1 hora

# Configurações de email (para notificações)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')