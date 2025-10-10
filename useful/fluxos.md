🔐 Fluxo de Autenticação
```mermaid
sequenceDiagram
    participant F as Frontend (Browser)
    participant D as Django Monolith
    participant A as Auth Service
    participant DB as PostgreSQL

    F->>F: Usuário preenche login/senha
    F->>D: POST /api/auth/login {username, password}
    D->>A: POST /api/auth/login {username, password}
    A->>DB: SELECT user WHERE username=?
    DB-->>A: Retorna user_id e hash senha
    A->>A: Valida senha com passlib
    A->>A: Cria JWT token (exp: 1h)
    A-->>D: {token: "eyJ..."}
    D-->>F: {token: "eyJ..."}
    F->>F: Armazena token em sessionStorage
    
    Note over F: Próximas requisições incluem token
    
    F->>D: GET /api/patients/<br/>Header: Bearer token
    D->>D: Executa decorator @jwt_required
    D->>A: GET /api/auth/validate<br/>Header: Bearer token
    A->>A: Decodifica e valida JWT
    A-->>D: {user_id: 123, permissions: [...]}
    D->>D: Adiciona user_data à request
    D->>DB: SELECT patient data
    DB-->>D: Retorna dados
    D-->>F: JSON com dados do paciente```