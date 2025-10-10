# SGHSS-Sistema_de_gestao_hospitalar
Sistema de gestão hospitalar e de serviços de saúde

# 🏥 SGHSS - Sistema de Gestão Hospitalar e de Serviços de Saúde

## 📋 Guia de Instalação e Configuração

Este documento descreve como configurar e executar o sistema SGHSS, incluindo a conexão entre frontend, backend e serviço de autenticação.

---

## 🏗️ Arquitetura do Sistema

```
┌─────────────────┐
│    Frontend     │
│   (HTML/JS)     │
└────────┬────────┘
         │ HTTP Requests
         │ (JWT Token)
         ↓
┌─────────────────┐
│ Django Monolith │ ←──┐
│  (Backend API)  │    │ Valida Token
└────────┬────────┘    │
         │             │
         │ Autentica   │
         │ Usuário     │
         ↓             │
┌─────────────────────┐│
│ Authentication      ││
│ Service (Flask)     ││
└─────────────────────┘
         │
         ↓
┌─────────────────┐
│   PostgreSQL    │
│   (Database)    │
└─────────────────┘
```

---

## 📦 Pré-requisitos

### Backend
- Python 3.9+
- PostgreSQL 12+
- Docker e Docker Compose (recomendado)

### Frontend
- Navegador moderno (Chrome, Firefox, Edge)
- Servidor HTTP local (Live Server, http-server, etc.)

---

## 🚀 Instalação

### 1️⃣ Configurar o Backend

#### **Opção A: Usando Docker (Recomendado)**

```bash
# Navegue até a pasta backend
cd backend

# Inicie os serviços com Docker Compose
docker-compose up -d

# Aguarde os serviços iniciarem
# Django Monolith estará em: http://localhost:8000
# Authentication Service estará em: http://localhost:8001
```

#### **Opção B: Instalação Manual**

**Django Monolith:**

```bash
# Navegue até a pasta do monolith
cd backend/sghss-monolith

# Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com suas configurações

# Execute as migrações
python manage.py migrate

# Crie um superusuário
python manage.py createsuperuser

# Inicie o servidor
python manage.py runserver 0.0.0.0:8000
```

**Authentication Service:**

```bash
# Em outro terminal, navegue até authentication-service
cd backend/authentication-service

# Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com suas configurações

# Inicie o serviço
python app.py
```

---

### 2️⃣ Configurar o Frontend

```bash
# Navegue até a pasta frontend
cd frontend

# Configure o arquivo de configuração
# Edite o arquivo config.js e defina as URLs corretas:
# - MONOLITH_URL: URL do Django (padrão: http://localhost:8000)
# - AUTH_SERVICE_URL: URL do serviço de autenticação (padrão: http://localhost:8001)
```

#### **Estrutura de Arquivos Frontend:**

```
frontend/
├── index.html              # Página de login
├── dashboard.html          # Dashboard principal
├── cadastro.html           # Cadastro de usuários
├── pacientes.html          # Gestão de pacientes
├── telemedicina.html       # Telemedicina
├── javascript/
│   ├── config.js          # ⭐ Configurações da API (IMPORTANTE)
│   ├── login.js           # ⭐ Sistema de autenticação (NOVO)
│   ├── exemplos_requisicoes.js  # Exemplos de uso
│   ├── cadastro.js        # Lógica de cadastro
│   └── ...outros arquivos
└── styles/
    └── ...arquivos CSS
```

#### **Servir o Frontend:**

**Opção A: Live Server (VS Code)**
1. Instale a extensão "Live Server" no VS Code
2. Clique com botão direito em `index.html`
3. Selecione "Open with Live Server"

**Opção B: http-server (Node.js)**
```bash
# Instale o http-server globalmente
npm install -g http-server

# Navegue até a pasta frontend
cd frontend

# Inicie o servidor
http-server -p 8080

# Acesse: http://localhost:8080
```

**Opção C: Python SimpleHTTPServer**
```bash
# Python 3
cd frontend
python -m http.server 8080

# Acesse: http://localhost:8080
```

---

## 🔐 Configuração de Autenticação

### Variáveis de Ambiente

#### **Django Monolith (.env)**
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/sghss_db

# Authentication Service
AUTH_SERVICE_VALIDATE_URL=http://authentication-service:8001/api/auth/validate

# Security
SECRET_KEY=sua-secret-key-super-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS (Permitir requisições do frontend)
CORS_ALLOWED_ORIGINS=http://localhost:8080,http://127.0.0.1:8080
```

#### **Authentication Service (.env)**
```env
# Database
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=sghss_db
POSTGRES_USER=user
POSTGRES_PASSWORD=password

# JWT
SECRET_KEY=mesma-secret-key-do-django
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=1

# Flask
FLASK_ENV=development
FLASK_DEBUG=True
```

---

## 🧪 Testando a Conexão

### 1. Testar o Backend

```bash
# Teste o endpoint de login do Django
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"00000000000","password":"admin123"}'

# Resposta esperada:
# {"token":"eyJ0eXAiOiJKV1QiLCJhbGc..."}
```

### 2. Testar o Frontend

1. Abra o navegador em `http://localhost:8080`
2. Use as credenciais de teste:
   - **Administrador**: CPF `00000000000` | Senha `admin123`
   - **Médico**: CPF `33333333333` | Senha `medico123`
   - **Enfermeiro**: CPF `11111111111` | Senha `enfermeiro123`
   - **Paciente**: CPF `22222222222` | Senha `paciente123`

3. Abra o Console do Navegador (F12) para ver os logs de debug

---

## 📝 Uso do Sistema de Autenticação

### **Login**

O arquivo `login.js` gerencia automaticamente:
- Envio de credenciais para o backend
- Armazenamento seguro do token JWT
- Redirecionamento após login
- Validação de sessão

### **Requisições Autenticadas**

Use a função `fetchAutenticado()` para fazer requisições protegidas:

```javascript
// Exemplo: Buscar lista de pacientes
async function buscarPacientes() {
  try {
    const response = await window.fetchAutenticado(
      window.API_CONFIG.API_ENDPOINTS.PATIENTS_LIST,
      { method: 'GET' }
    );
    
    if (response.ok) {
      const pacientes = await response.json();
      console.log('Pacientes:', pacientes);
    }
  } catch (error) {
    console.error('Erro:', error);
  }
}
```

### **Verificar Autenticação**

```javascript
// Proteger páginas que requerem login
if (!window.verificarAutenticacao()) {
  window.location.href = 'index.html';
}
```

### **Logout**

```javascript
// Fazer logout
window.realizarLogout();
```

---

## 🔒 Segurança

### **Boas Práticas Implementadas**

✅ **JWT Token**: Autenticação baseada em tokens seguros  
✅ **HTTPS**: Use sempre HTTPS em produção  
✅ **SessionStorage**: Tokens armazenados em sessionStorage (mais seguro que localStorage)  
✅ **CORS**: Configurado para permitir apenas origens confiáveis  
✅ **Validação**: Tokens validados em cada requisição  
✅ **Expiração**: Tokens expiram automaticamente após 1 hora  
✅ **Proteção CSRF**: Django protege contra ataques CSRF  

### **Considerações Adicionais**

⚠️ **Produção**: Altere `SECRET_KEY` para um valor aleatório e seguro  
⚠️ **HTTPS**: Nunca use HTTP em produção  
⚠️ **Logs**: Desabilite `DEBUG=False` em produção  
⚠️ **CORS**: Configure `CORS_ALLOWED_ORIGINS` para domínios específicos  

---

## 🛠️ Troubleshooting

### **Problema: Erro de CORS**

```
Access to fetch at 'http://localhost:8000/api/auth/login/' from origin 'http://localhost:8080'
has been blocked by CORS policy
```

**Solução:**
1. Instale `django-cors-headers` no Django:
   ```bash
   pip install django-cors-headers
   ```

2. Adicione no `settings.py`:
   ```python
   INSTALLED_APPS = [
       ...
       'corsheaders',
   ]
   
   MIDDLEWARE = [
       'corsheaders.middleware.CorsMiddleware',
       ...
   ]
   
   CORS_ALLOWED_ORIGINS = [
       "http://localhost:8080",
       "http://127.0.0.1:8080",
   ]
   ```

### **Problema: Token inválido ou expirado**

**Sintoma:** Redirecionamento automático para login

**Solução:** Isso é normal. O token expira após 1 hora. Faça login novamente.

### **Problema: Erro 500 no backend**

**Solução:**
1. Verifique os logs do Django: `docker logs sghss-monolith`
2. Verifique se o PostgreSQL está rodando
3. Verifique se as migrations foram executadas

### **Problema: Serviço de autenticação não responde**

**Solução:**
1. Verifique se o serviço está rodando: `docker ps`
2. Verifique os logs: `docker logs authentication-service`
3. Verifique a conexão com PostgreSQL

---

## 📚 Próximos Passos

1. ✅ Implementar recuperação de senha
2. ✅ Adicionar refresh tokens para renovação automática
3. ✅ Implementar 2FA (autenticação de dois fatores)
4. ✅ Adicionar rate limiting para prevenir ataques de força bruta
5. ✅ Implementar logs de auditoria de acesso

---

## 📞 Suporte

Para dúvidas ou problemas:
- 📧 Email: viniciustasso@live.com
- 🌐 Website: https://www.linkedin.com/in/vinitasso/

---

## 📄 Licença

Copyright © 2025 Vinicius Tasso - Todos os direitos reservados.