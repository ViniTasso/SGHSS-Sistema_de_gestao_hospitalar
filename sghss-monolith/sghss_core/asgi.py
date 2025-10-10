"""
asgi.py - ASGI Configuration for SGHSS

ASGI (Asynchronous Server Gateway Interface) é o sucessor do WSGI.
Suporta aplicações assíncronas, WebSockets, e HTTP/2.

Este arquivo expõe o callable ASGI como uma variável no nível do módulo chamada 'application'.

Para mais informações sobre este arquivo, veja:
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Define qual settings.py usar
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sghss_core.settings')

# Obtém a aplicação ASGI do Django
application = get_asgi_application()
