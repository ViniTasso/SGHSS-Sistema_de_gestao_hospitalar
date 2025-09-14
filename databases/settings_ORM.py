# sghss_monolith/sghss_core/settings.py
# PRECISA DO FRAMEWORK JANGO PARA FAZER USO DO ORM
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
