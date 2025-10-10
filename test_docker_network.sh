#!/bin/bash

# ==================== SCRIPT DE TESTE - DOCKER NETWORK SGHSS ====================
# Este script testa se os containers estão se comunicando corretamente
# Execute com: bash test_docker_network.sh

echo "🐳 ==================== TESTE DE NETWORK DOCKER SGHSS ===================="
echo ""

# Cores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para verificar se comando teve sucesso
check_result() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ SUCESSO${NC}"
        return 0
    else
        echo -e "${RED}❌ FALHOU${NC}"
        return 1
    fi
}

# ==================== TESTE 1: Verificar se containers estão rodando ====================
echo -e "${BLUE}📋 Teste 1: Verificando containers ativos...${NC}"
docker compose ps
echo ""

# ==================== TESTE 2: Verificar variáveis de ambiente ====================
echo -e "${BLUE}📋 Teste 2: Verificando variáveis de ambiente do Django...${NC}"
echo "POSTGRES_HOST:"
docker exec sghss-monolith env | grep POSTGRES_HOST
check_result

echo "AUTH_SERVICE_VALIDATE_URL:"
docker exec sghss-monolith env | grep AUTH_SERVICE_VALIDATE_URL
check_result
echo ""

# ==================== TESTE 3: Testar conexão Django -> PostgreSQL ====================
echo -e "${BLUE}📋 Teste 3: Testando conexão Django -> PostgreSQL...${NC}"
docker exec sghss-monolith python manage.py check --database default
check_result
echo ""

# ==================== TESTE 4: Testar DNS interno (ping) ====================
echo -e "${BLUE}📋 Teste 4: Testando DNS interno (ping entre containers)...${NC}"

echo "Ping db-postgres:"
docker exec sghss-monolith ping -c 2 db-postgres > /dev/null 2>&1
check_result

echo "Ping authentication-service:"
docker exec sghss-monolith ping -c 2 authentication-service > /dev/null 2>&1
check_result
echo ""

# ==================== TESTE 5: Testar curl entre containers ====================
echo -e "${BLUE}📋 Teste 5: Testando comunicação HTTP (curl)...${NC}"

echo "Django -> Auth Service:"
docker exec sghss-monolith curl -s -o /dev/null -w "%{http_code}" http://authentication-service:8001/api/auth/validate
echo ""
check_result
echo ""

# ==================== TESTE 6: Testar PostgreSQL diretamente ====================
echo -e "${BLUE}📋 Teste 6: Testando PostgreSQL diretamente...${NC}"
docker exec db-postgres pg_isready -U postgres
check_result
echo ""

# ==================== TESTE 7: Verificar se Django está respondendo ====================
echo -e "${BLUE}📋 Teste 7: Testando se Django está respondendo...${NC}"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8050)
echo "HTTP Status Code: $HTTP_CODE"
if [ "$HTTP_CODE" -eq 200 ] || [ "$HTTP_CODE" -eq 301 ] || [ "$HTTP_CODE" -eq 302 ]; then
    check_result
else
    echo -e "${RED}❌ Django não está respondendo corretamente${NC}"
fi
echo ""

# ==================== TESTE 8: Verificar logs de erro ====================
echo -e "${BLUE}📋 Teste 8: Verificando logs recentes do Django...${NC}"
echo "Últimas 10 linhas de log:"
docker compose logs --tail=10 sghss-monolith
echo ""

# ==================== TESTE 9: Testar endpoint de login ====================
echo -e "${BLUE}📋 Teste 9: Testando endpoint de login...${NC}"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test"}')
echo "HTTP Status Code: $HTTP_CODE"
if [ "$HTTP_CODE" -eq 200 ] || [ "$HTTP_CODE" -eq 401 ] || [ "$HTTP_CODE" -eq 400 ]; then
    echo -e "${GREEN}✅ Endpoint está respondendo${NC}"
else
    echo -e "${RED}❌ Endpoint não está respondendo corretamente${NC}"
fi
echo ""

# ==================== RESUMO ====================
echo -e "${YELLOW}📊 ==================== RESUMO DOS TESTES ====================${NC}"
echo ""
echo "Se todos os testes passaram, seu ambiente Docker está configurado corretamente!"
echo ""
echo "Se algum teste falhou, verifique:"
echo "1. Se todos os containers estão rodando: docker-compose ps"
echo "2. Logs dos containers: docker-compose logs [nome-do-container]"
echo "3. Se as variáveis de ambiente estão corretas no docker-compose.yml"
echo "4. Se o settings.py está usando os nomes corretos dos serviços"
echo ""
echo -e "${BLUE}Para ver logs em tempo real:${NC}"
echo "  docker-compose logs -f sghss-monolith"
echo ""
echo -e "${BLUE}Para entrar em um container:${NC}"
echo "  docker exec -it sghss-monolith bash"
echo ""
echo "🐳 ==================== FIM DOS TESTES ===================="