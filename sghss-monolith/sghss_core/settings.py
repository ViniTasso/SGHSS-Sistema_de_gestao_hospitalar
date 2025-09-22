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
    # Adicione seus novos módulos aqui
    'accounts.apps.AccountsConfig',
    'patients.apps.PatientsConfig',
]

AUTH_USER_MODEL = 'accounts.User' #O AUTH_USER_MODEL é crucial para dizer ao Django que a sua classe User personalizada é a que deve ser usada para o sistema de autenticação.