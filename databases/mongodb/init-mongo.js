db = db.getSiblingDB('auth_db');

// Cria a coleção de logs de auditoria
db.createCollection('audit_logs');
db.audit_logs.createIndex({ user_id: 1, created_at: -1 });

// Insere alguns dados de exemplo (opcional)
db.audit_logs.insertMany([
  {
    "user_id": "c0926868-d3c2-4a0b-967a-11e403487c9d",
    "action": "login",
    "resource": "api/auth/login",
    "timestamp": new Date()
  },
  {
    "user_id": "c0926868-d3c2-4a0b-967a-11e403487c9d",
    "action": "access",
    "resource": "prontuario/123",
    "timestamp": new Date()
  }
]);
