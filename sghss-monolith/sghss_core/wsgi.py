"""
wsgi.py - WSGI Configuration for SGHSS

WSGI (Web Server Gateway Interface) é o padrão Python para servidores web.
Este arquivo expõe o callable WSGI como uma variável no nível do módulo chamada 'application'.

Para mais informações sobre este arquivo, veja:
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Define qual settings.py usar
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sghss_core.settings')

# Obtém a aplicação WSGI do Django
application = get_wsgi_application()
