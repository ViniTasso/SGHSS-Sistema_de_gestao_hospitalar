#!/bin/bash

# ==================== SCRIPT DE PADRONIZAÇÃO SGHSS ====================
# Este script cria os arquivos faltantes e padroniza o projeto
# Execute com: bash setup_standardization.sh

# Cores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🎯 ==================== PADRONIZAÇÃO SGHSS ====================${NC}"
echo ""

# ==================== PASSO 1: Criar wsgi.py ====================
echo -e "${YELLOW}📝 Passo 1: Criando wsgi.py...${NC}"

DIR_OF_SCRIPT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

WSGI_PATH="$DIR_OF_SCRIPT/sghss_core/wsgi.py"

#WSGI_PATH="SGHSS-Sistema_de_gestao_hospitalar/sghss-monolith/sghss_core/wsgi.py"

if [ -f "$WSGI_PATH" ]; then
    echo -e "${YELLOW}⚠️  wsgi.py já existe. Pulando...${NC}"
else
    #mkdir -p "/sghss_core"
    cat > "$WSGI_PATH" << 'EOF'
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
EOF
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ wsgi.py criado com sucesso!${NC}"
    else
        echo -e "${RED}❌ Erro ao criar wsgi.py${NC}"
        exit 1
    fi
fi

echo ""

# ==================== PASSO 2: Criar asgi.py ====================
echo -e "${YELLOW}📝 Passo 2: Criando asgi.py...${NC}"

#ASGI_PATH="SGHSS-Sistema_de_gestao_hospitalar/sghss-monolith/sghss_core/asgi.py"
ASGI_PATH="$DIR_OF_SCRIPT/sghss_core/asgi.py"

if [ -f "$ASGI_PATH" ]; then
    echo -e "${YELLOW}⚠️  asgi.py já existe. Pulando...${NC}"
else
    cat > "$ASGI_PATH" << 'EOF'
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
EOF
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ asgi.py criado com sucesso!${NC}"
    else
        echo -e "${RED}❌ Erro ao criar asgi.py${NC}"
        exit 1
    fi
fi

echo ""

# ==================== PASSO 3: Verificar estrutura ====================
echo -e "${YELLOW}🔍 Passo 3: Verificando estrutura de arquivos...${NC}"

if [ -f "$DIR_OF_SCRIPT/sghss-monolith/sghss_core/__init__.py" ]; then
    echo -e "${GREEN}✅ __init__.py existe${NC}"
else
    echo -e "${RED}❌ __init__.py não encontrado${NC}"
fi

if [ -f "$DIR_OF_SCRIPT/sghss-monolith/sghss_core/settings.py" ]; then
    echo -e "${GREEN}✅ settings.py existe${NC}"
else
    echo -e "${RED}❌ settings.py não encontrado${NC}"
fi

if [ -f "$DIR_OF_SCRIPT/sghss-monolith/sghss_core/urls.py" ]; then
    echo -e "${GREEN}✅ urls.py existe${NC}"
else
    echo -e "${RED}❌ urls.py não encontrado${NC}"
fi

if [ -f "$WSGI_PATH" ]; then
    echo -e "${GREEN}✅ wsgi.py existe${NC}"
else
    echo -e "${RED}❌ wsgi.py não encontrado${NC}"
fi

if [ -f "$ASGI_PATH" ]; then
    echo -e "${GREEN}✅ asgi.py existe${NC}"
else
    echo -e "${RED}❌ asgi.py não encontrado${NC}"
fi

echo ""

# ==================== PASSO 4: Verificar requirements.txt ====================
echo -e "${YELLOW}📦 Passo 4: Verificando requirements.txt...${NC}"

# Django
if grep -q "Django==4.2.7" $DIR_OF_SCRIPT/sghss-monolith/requirements.txt; then
    echo -e "${GREEN}✅ Django listado em requirements.txt${NC}"
else
    echo -e "${RED}❌ Django não encontrado em requirements.txt${NC}"
fi

# Flask
if grep -q "Flask==3.0.0" $DIR_OF_SCRIPT/authentication-service/requirements.txt; then
    echo -e "${GREEN}✅ Flask listado em requirements.txt${NC}"
else
    echo -e "${RED}❌ Flask não encontrado em requirements.txt${NC}"
fi

echo ""

# ==================== PASSO 5: Instruções de rebuild ====================
echo -e "${BLUE}🐳 Próximos passos:${NC}"
echo ""
echo "1. Parar os containers:"
echo "   ${YELLOW}docker-compose down${NC}"
echo ""
echo "2. Rebuild os containers:"
echo "   ${YELLOW}docker-compose up --build${NC}"
echo ""
echo "3. Executar migrations:"
echo "   ${YELLOW}docker-compose exec sghss-monolith python manage.py migrate${NC}"
echo ""
echo "4. Verificar se está funcionando:"
echo "   ${YELLOW}curl http://localhost:8000/admin/${NC}"
echo ""

# ==================== RESUMO ====================
echo -e "${GREEN}✅ ==================== PADRONIZAÇÃO CONCLUÍDA ====================${NC}"
echo ""
echo "Arquivos criados:"
echo "  - backend/sghss-monolith/sghss_core/wsgi.py"
echo "  - backend/sghss-monolith/sghss_core/asgi.py"
echo ""
echo "Execute os próximos passos acima para finalizar!"
echo ""