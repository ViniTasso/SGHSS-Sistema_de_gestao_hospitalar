#!/bin/bash
# SGHSS Project Automation Script

# --- Variáveis de Configuração ---
MONO_SERVICE="sghss-monolith"
AUTH_SERVICE="authentication-service"
AI_SERVICE="ai-service"
DB_POSTGRES="db-postgres"
DB_MONGO="db-mongodb"


# Lista de portas da aplicação para checagem
APP_PORTS=(8001 8002 8003 5432 27017)
# --- Variáveis de Configuração de Porta (Host) ---
MONO_PORT=8050
AUTH_PORT=8060

#set -e
#cd "$(dirname "$0")"

# --- Funções de Utilitário ---

# Cores para o terminal
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
BLACK='\033[0;34m';
NC='\033[0m' # No Color

warn() { echo -e "${YELLOW}[!] WARNING:${NC} $1"; }
info() { echo -e "${GREEN}[INFO]:${NC} $1"; }
error() { echo -e "${RED}[ERROR]:${NC} $1"; }
success() { echo -e "${GREEN}✓${NC} $1"; }
log() { echo -e "${GREEN}[$(date '+%H:%M:%S')]${NC} $1"; }
# # Cores
# error() { echo -e "${R}[ERROR]${NC} $1"; exit 1; }

# Carregar .env se existir
load_env() {
    set -a;
    source ./app/.env;
    set +a;
}

# Verificar portas ocupadas
check_ports() {
    local busy=()
    for port in "${APP_PORTS[@]}"; do
        # O comando lsof ou fuser precisa estar instalado
        if command -v lsof &> /dev/null; then
            lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1 && busy+=($port)
        elif command -v fuser &> /dev/null; then
            fuser -k -n tcp "$port" >/dev/null 2>&1 && busy+=($port)
        fi
    done
    if [ ${#busy[@]} -gt 0 ]; then
        warn "Portas ocupadas: ${busy[*]}"
        error "O processo de startup pode falhar. Por favor, libere-as manualmente."
        echo "Execute 'sudo bash run.sh clean' primeiro ou:"
        echo "sudo fuser -k ${busy[*]/%//tcp}"
        read -r -p "Deseja continuar mesmo assim? (y/N): " REPLY
        [[ ! $REPLY =~ ^[Yy]$ ]] && exit 1
    fi
}

# Comando: status - Checa o status dos containers
status() {
    info "Status atual dos containers:"
    docker compose ps
}

# -----------------------------------------------------

# Comando: build - Constrói e Inicia os Dockers
build() {
    check_ports
    info "Construindo e iniciando todos os serviços..."
    docker compose up -d --build
    status
}

# Comando: down - Derruba os Dockers
down() {
    info "Derrubando containers..."
    docker compose down
}

# Comando: clean - Derruba e Limpa volumes (para recomeçar do zero)
clean-docker() {
    info "Limpando todos os containers e volumes de dados (perda de dados não persistidos)..."
    docker compose down --volumes
}

# Comando: rebuild_service - Reconstroi um serviço específico
rebuild_service() {
    local service=$1
    if [[ -z "$service" ]]; then
        error "Uso: rebuild_service <nome_do_serviço>"
        return 1
    fi
    info "Reconstruindo e reiniciando o serviço: $service"
    # --no-deps: Ignora dependências (útil para microsserviços)
    docker compose up -d --build --no-deps "$service"
}

# Comando: rebuild - Rebuild completo
rebuild() {
    echo "REBUILD SYSTEM"
    echo "=============="
    
    log "Parando serviços..."
    docker-compose down 2>/dev/null || true
    
    log "Rebuild sem cache..."
    docker-compose build --no-cache
    
    success "Rebuild concluído!"
    echo "Use 'sudo bash run.sh dev' ou 'sudo bash run.sh prod' para iniciar"
}

# -----------------------------------------------------

# Comando: migrate - Roda as migrações do Django
migrate() {
    info "Rodando migrações (makemigrations e migrate)..."
    docker compose run --rm "$MONO_SERVICE" python manage.py makemigrations accounts patients
    docker compose run --rm "$MONO_SERVICE" python manage.py migrate
}

# Comando: seed - Roda o script de seed de permissões
seed_data() {
    info "Populando banco de dados com Roles e Permissões (seed)..."
    # O script seed_permissions.py está dentro da pasta seed/
    docker compose run --rm "$MONO_SERVICE" python seed/seed_permissions.py
}

register_patient(){
    #curl -X POST http://localhost:8050/api/patients/register/ -H "Content-Type: application/json" -d '{"username": "joao.silva","password": "senha123","nome_completo": "João da Silva","cpf": "123.456.789-00"}'

    # Gera uma string única baseada no timestamp para evitar erros de duplicidade
    local RANDOM_ID=$(date +%s%N | cut -b1-8)
    local USERNAME="test.user.$RANDOM_ID"
    
    # Extrai os primeiros 3 dígitos (para a 1ª parte)
    local PARTE_UNICA_1="${RANDOM_ID:0:3}"

    # Extrai os próximos 3 dígitos (para a 2ª parte)
    local PARTE_UNICA_2="${RANDOM_ID:3:3}"

    # Extrai os últimos 2 dígitos (para o dígito verificador)
    local VERIFICADOR="${RANDOM_ID:6:2}"

    # Constrói o CPF (exemplo: 123.456.789-01)
    local CPF="000.${PARTE_UNICA_1}.${PARTE_UNICA_2}-${VERIFICADOR}"

    info 'Cadastrando paciente de teste: "'"$USERNAME"'" na porta "'"$MONO_PORT"'"...
            CPF: "'"$CPF"'".
            Nome Completo: Paciente Teste '$RANDOM_ID''

    # O comando curl com os dados dinâmicos.
    # Note o uso de aspas simples e duplas para Bash e JSON.
    curl -X POST "http://localhost:$MONO_PORT/api/patients/register/" \
      -H "Content-Type: application/json" \
      -d '{
        "username": "'"$USERNAME"'",
        "password": "testpassword",
        "nome_completo": "Paciente Teste '"$RANDOM_ID"'",
        "cpf": "'"$CPF"'"
      }'
    echo "" # Nova linha para organizar o terminal

}

# Comando: test_access - Testa a rota de acesso ao prontuário para uma lista de IDs
test_access() {
    #API CURL
    #curl -X GET http://localhost:8050/api/patients/5e8c12a5-6353-4a72-96da-d6f77fd5310e/ -H "Authorization: Bearer seu-jwt-aqui"

    # ATENÇÃO: Substitua [SEU-TOKEN-AQUI] pelo token real
    local TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZGQwNTdhN2UtZGI5NS00OTc3LWJkZWYtNWE5NTkxZjQ0MmUzIiwiZXhwIjoxNzU5Njc3MjU5LCJpYXQiOjE3NTk2NzM2NTl9.EJZ9cRaiSRAWXsPXxjw7t24F1ZSHm-jAXMsUrHoOssk"

    # Lista de IDs para testar. O primeiro ID deve ser um paciente válido.
    # O último ID pode ser um UUID inexistente (para testar 404).
    # AJUSTAR ESTA LISTA com os UUIDs reais
    local PATIENT_IDS=(
        "91075dee-eb91-42d8-97d2-c8bf2766e963"  # Paciente cadastrado (acesso esperado)
        "0888f4a8-4a54-42e3-a8b3-118fedb191cc"  # Outro paciente cadastrado
        "00000000-0000-0000-0000-000000000000"  # Exemplo de ID inexistente (esperado 404)
    )

    local API_URL="http://localhost:$MONO_PORT/api/patients/"

    info "Iniciando teste de acesso (Verificação de Authorization e Permissão)..."

    for patient_id in "${PATIENT_IDS[@]}"; do
        echo -e "${YELLOW}--- Testando ID: $patient_id ---${NC}"
        
        # Executa o curl e armazena o código de status na variável STATUS_CODE
        # -s: Modo silencioso
        # -o /dev/null: Descarta o corpo da resposta
        # -w "%{http_code}": Escreve apenas o código HTTP
        STATUS_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
          -X GET "$API_URL$patient_id/" \
          -H "Authorization: Bearer $TOKEN")

        # Análise do Status Code
        if [ "$STATUS_CODE" -eq 200 ]; then
            echo -e "${GREEN}SUCESSO:${NC} Status $STATUS_CODE. Acesso Concedido."
        elif [ "$STATUS_CODE" -eq 403 ]; then
            echo -e "${RED}FALHA:${NC} Status $STATUS_CODE. Permissão Negada (403)."
        elif [ "$STATUS_CODE" -eq 401 ]; then
            echo -e "${RED}FALHA:${NC} Status $STATUS_CODE. Não Autorizado (401). (Token Inválido/Expirado)"
        elif [ "$STATUS_CODE" -eq 404 ]; then
            echo -e "${RED}ERRO:${NC} Status $STATUS_CODE. Recurso Não Encontrado (404)."
        else
            echo -e "${YELLOW}AVISO:${NC} Status $STATUS_CODE. Resposta Inesperada. Cheque os logs."
        fi
    done
    echo -e "${GREEN}--- Teste de Acesso Concluído ---${NC}"
    echo -e "${YELLOW}TIPS: Para mais info: docker compose logs <sghss-monolith> ou <authentication-service> ---${NC}"
}

# Comando: db_shell - Entra no shell do PostgreSQL
db_shell() {
    info "Acessando shell do PostgreSQL..."
    #Junção do:
    # docker compose exec -it db-postgres bash
    #Com o:
    #psql -U user -d sghss_db
    docker compose exec -it "$DB_POSTGRES" psql -U user -d sghss_db
}

# Comando: mongo_shell - Entra no shell do MongoDB (requer o shell instalado localmente ou dentro do container)
mongo_shell() {
    info "Tentando acessar o shell do MongoDB (Admin DB)..."
    # Este comando assume que você pode usar o mongosh/mongo a partir do host
    # Se falhar, use 'docker compose exec -it db-mongodb bash' para entrar no container
    mongosh "mongodb://user:password@localhost:27017/auth_db" --authenticationDatabase admin
}

# Comando: dev - Desenvolvimento com hot reload
dev() {
    echo "TRANSCRIPTOR - DESENVOLVIMENTO"
    echo "=================================="
    
    [ ! -f "app/.env" ] && error "Arquivo app/.env não encontrado!"
    
    check_ports
    
    log "Preparando ambiente..."
    mkdir -p data/{uploads,processing,results,logs}
    docker-compose down --remove-orphans 2>/dev/null || true
    
    log "Build das imagens..."
    docker-compose build
    
    echo ""
    echo "Iniciando desenvolvimento..."
    echo ""
    echo "Serviços:"
    echo "  App Principal: http://localhost:5000"
    echo "  Flower: http://localhost:5555"  
    echo "  Redis Commander: http://localhost:8081 (admin/redis123)"
    echo ""
    echo "Comandos úteis:"
    echo "  sudo bash run.sh logs           # Ver logs"
    echo "  sudo bash run.sh logs web       # Logs específicos"
    echo "  sudo bash run.sh clean          # Parar tudo"
    echo ""
    echo "  Pressione Ctrl+C para parar"
    echo ""
    
    docker-compose --profile dev up
}

# Comando: prod - Produção (background)
prod() {
    echo "TRANSCRIPTOR - PRODUÇÃO"
    echo "=========================="
    
    [ ! -f "app/.env" ] && error "Arquivo app/.env não encontrado!"
    
    log "Preparando produção..."
    mkdir -p data/{uploads,processing,results,logs}
    docker-compose down --remove-orphans 2>/dev/null || true
    
    log "Build otimizado..."
    docker-compose build --no-cache
    
    log "Iniciando em background..."
    docker-compose --profile dev up -d
    
    echo ""
    success "Produção iniciada!"
    echo "Aplicação: http://localhost:5000"
    echo ""
    echo "Comandos:"
    echo "  ./run status    # Status dos containers"
    echo "  ./run logs      # Ver logs"
    echo "  ./run clean     # Parar"
}

# Comando: clean - Limpar ambiente
clean() {
    echo "LIMPEZA DO PROJETO ATUAL"
    echo "========================"
    
    log "Interrompendo serviços..."
    docker compose down --remove-orphans 2>/dev/null || true
    #2>/dev/null faz uma saída limpa, envia logs para o local, que elimina as info.
    # || true garante que o código seguinte seja executado mesmo com false(erro) do docker compose
    
    # Containers específicos (caso existam fora do compose)
    # local containers=(container1 container2)
    # for c in "${containers[@]}"; do
    #     docker stop "$c" 2>/dev/null || true
    #     docker rm "$c" 2>/dev/null || true
    # done
    
    log "Liberando portas..."
    for port in "${APP_PORTS[@]}"; do
        sudo fuser -k $port/tcp 2>/dev/null || true
    done
    
    #"$1" consegue pegar o parầmetro passado na hora de executar o comando
    #. run.sh --full - Se houver o parâmetro ele executa o código a seguir
    if [ "$1" = "--full" ]; then
        log "Limpeza completa..."
        docker images --format "{{.Repository}}:{{.Tag}}" | grep transcription | xargs -r docker rmi 2>/dev/null || true
        docker system prune -f
        
        # Limpar dados (preservar .gitkeep)
        for dir in uploads processing results logs; do
            [ -d "data/$dir" ] && find "data/$dir" -type f ! -name '.gitkeep' -delete 2>/dev/null || true
        done
    fi
    
    success "Limpeza concluída!"
}

# Comando: logs - Ver logs
logs() {
    # case "${1:-all}" in
    #     web)        docker-compose logs -f web --tail=50 ;;
    #     worker)     docker-compose logs -f worker --tail=50 ;;
    #     redis)      docker-compose logs -f redis --tail=50 ;;
    #     flower)     docker-compose logs -f flower --tail=50 ;;
    #     all|*)      docker-compose logs -f --tail=50 ;;
    # esac

    local service=$1
    if [[ -z "$service" || "$service" == "all" ]]; then
        info "Exibindo logs de todos os serviços (últimas 50 linhas)..."
        docker compose logs -f --tail=50
    else
        info "Exibindo logs do serviço: $service..."
        docker compose logs -f --tail=50 "$service"
    fi
}

# Comando: status - Status dos containers
status() {
    echo "STATUS TRANSCRIPTOR"
    echo "===================="
    
    if docker-compose ps | grep -q "Up"; then
        docker-compose ps
        echo ""
        echo "URLs:"
        echo "  App: http://localhost:5000"
        echo "  Flower: http://localhost:5555"
        echo "  Redis Commander: http://localhost:8081"
    else
        echo "Nenhum container rodando"
        echo "Execute 'sudo bash run.sh dev' ou 'sudo bash run.sh prod'"
    fi
}

revert_last_commit() {
    git reset --soft HEAD~1
}

# Comando: deploy - Deploy simplificado
deploy() {
    load_env
    
    echo "DEPLOY TRANSCRIPTOR COM TRAEFIK"
    echo "===================="
    
    # Validar configurações
    [ -z "$VPS_HOST" ] && error "VPS_HOST não configurado no .env"
    [ -z "$VPS_USER" ] && error "VPS_USER não configurado no .env"
    [ -z "$VPS_SSH_KEY" ] && error "VPS_SSH_KEY não configurado no .env"
    [ -z "$DEPLOY_DIR" ] && error "DEPLOY_DIR não configurado no .env"
    
    local ssh_opts="-i $VPS_SSH_KEY -p ${VPS_PORT:-22} -o StrictHostKeyChecking=no -o ConnectTimeout=10"
    
    case "${1:-update}" in
        install)
            log "Instalando Docker no servidor..."
            ssh_exec "command -v docker >/dev/null || curl -fsSL https://get.docker.com | sh"
            ssh_exec "command -v docker-compose >/dev/null || (curl -L \"https://github.com/docker/compose/releases/latest/download/docker-compose-\$(uname -s)-\$(uname -m)\" -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose)"
            
            log "Clonando repositório..."
            local repo_url="https://github.com/${GITHUB_USER}/${GITHUB_REPO}.git"
            [ "$GITHUB_PRIVATE" = "true" ] && [ -n "$GITHUB_TOKEN" ] && repo_url="https://${GITHUB_TOKEN}@github.com/${GITHUB_USER}/${GITHUB_REPO}.git"
            
            ssh_exec "rm -rf '$DEPLOY_DIR' && git clone '$repo_url' '$DEPLOY_DIR'"
            
            log "Iniciando aplicação..."
            ssh_exec "cd '$DEPLOY_DIR' && sudo bash run.sh prod"
            
            success "Instalação concluída!"
            echo "Acesse: https://sotahtech.com/transcription-app"
            ;;
            
        update)
            log "Atualizando código..."
            ssh_exec "cd '$DEPLOY_DIR' && git pull origin ${GITHUB_BRANCH:-main}"
            
            log "Reiniciando aplicação..."
            ssh_exec "cd '$DEPLOY_DIR' && sudo bash run.sh clean && sudo bash run.sh prod"
            
            success "Atualização concluída!"
            ;;
            
        ssh)
            log "Conectando via SSH..."
            ssh_connect
            ;;

        pull)
            log "Atualizando repo via SSH..."
            ssh_exec "cd '$DEPLOY_DIR' && git pull origin ${GITHUB_BRANCH:-main}"
            log "Reiniciando aplicação..."
            ssh_exec "cd '$DEPLOY_DIR' && docker-compose down --remove-orphans 2>/dev/null || true"
            ssh_exec "cd '$DEPLOY_DIR' && docker-compose --profile dev up -d"
            ssh_exec "cd '$DEPLOY_DIR' && systemctl restart nginx"
            ;;
            
        logs)
            log "Logs do servidor..."
            ssh_exec "cd '$DEPLOY_DIR' && sudo bash run.sh logs"
            ;;
            
        *)
            echo "Uso: sudo bash run.sh deploy [comando]"
            echo ""
            echo "Comandos:"
            echo "  install  - Nova instalação completa"
            echo "  update   - Atualizar código (padrão)"
            echo "  ssh      - Conectar via SSH"
            echo "  logs     - Ver logs do servidor"
            ;;
    esac
}

# Comando: help
_help() {
    echo -e "${GREEN}SGHSS Project Management Script - Comandos Disponíveis:${NC}"
    echo "--------------------------------------------------------"
    echo -e "${GREEN}Gerenciamento de Ambiente:${NC}"
    echo -e "  ${RED}run${NC} ................ Roda o projeto do zero (clean + build + migrate + seed)."
    echo -e "  ${YELLOW}build${NC} ............. Constrói e inicia todos os containers em background (-d)."
    echo -e "  ${RED}down${NC} ................ Derruba todos os containers (mantém os dados)."
    echo -e "  ${RED}clean${NC} .............. Derruba TUDO, incluindo volumes de dados (Reset Total)."
    echo -e "  ${YELLOW}rebuild <serviço>${NC} . Reconstroi e reinicia um serviço específico (e.g., mono, auth)."
    echo ""
    echo -e "${GREEN}Desenvolvimento e Dados:${NC}"
    echo -e "  ${YELLOW}migrate${NC} ............ Roda as migrações do Django (makemigrations + migrate)."
    echo -e "  ${YELLOW}seed${NC} ............... Popula o banco com Roles e Permissões."
    echo -e "  ${YELLOW}register-patient${NC} .. Cadastra um paciente com dados únicos para testes."

    echo ""
    echo -e "${GREEN}Diagnóstico e Shell:${NC}"
    echo -e "  ${YELLOW}status${NC} ............. Mostra o status de todos os containers."
    echo -e "  ${YELLOW}logs <serviço>${NC} ..... Exibe logs em tempo real (e.g., logs mono, logs auth, logs all)."
    echo -e "  ${YELLOW}db_shell${NC} .......... Abre o shell interativo do PostgreSQL."
    echo -e "  ${YELLOW}mongo_shell${NC} ....... Tenta acessar o shell do MongoDB (Admin)."
    echo -e "  ${YELLOW}check_ports${NC} ....... Verifica se as portas do projeto estão livres."

    echo ""
    echo -e "${GREEN}Pipiline de Testes:${NC}"
    echo -e "  ${YELLOW}test_access${NC} ............. Testa a rota de acesso ao prontuário para uma lista de IDs."

}


# -----------------------------------------------------


# Comando: run - Roda o projeto completo (Função principal recomendada)
run_project() {
    clean
    build
    migrate
    seed_data
    info "Projeto SGHSS está pronto e rodando!"
    status
}

# --- Main ---
main() {
    local cmd=$1
    local service_map=(
        ["mono"]="$MONO_SERVICE"
        ["auth"]="$AUTH_SERVICE"
        ["ai"]="$AI_SERVICE"
    )

    case "$cmd" in
        run)            run_project ;;
        build)          build ;;
        down)           down ;;
        clean)          clean ;;
        migrate)        migrate ;;
        seed)           seed_data ;;
        register-patient)register_patient ;;
        db_shell)       db_shell ;;
        mongo_shell)    mongo_shell ;;
        status)         status ;;
        check_ports)    check_ports ;;
        logs)           logs "${2:-all}" ;;
        rebuild)        rebuild_service "${service_map[${2}]}" ;;
        test_access)    test_access ;;
        -h|--help|help|*) _help ;;
    esac
}

main "$@"
