# sghss_monolith/sghss_core/settings.py

#É a configuração ORM
import os

# Definições do banco de dados
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sghss_db',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': 'db-postgres',  # O nome do serviço no docker-compose.yml
        'PORT': '5432',
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Adicione seus novos módulos a partir daqui
    #'accounts.apps.AccountsConfig',
    #'patients.apps.PatientsConfig',
    'accounts',
    'patients',
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
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ALLOWED_HOSTS = ['localhost', '127.0.0.1'] #Para resolver o erro de rodar em produção -->>> sghss-monolith          | CommandError: You must set settings.ALLOWED_HOSTS if DEBUG is False. sghss-monolith exited with code 1 
AUTH_USER_MODEL = 'accounts.User' #O AUTH_USER_MODEL é crucial para dizer ao Django que a sua classe User personalizada é a que deve ser usada para o sistema de autenticação.
ROOT_URLCONF = 'sghss_core.urls'
SECRET_KEY = 'MINHA_SECRET_KEY_QUE_NO_FIM_NAO_SERVE_PRA_NADA'