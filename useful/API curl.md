Registrar Paciente
curl -X POST http://localhost:8050/api/patients/register/ -H "Content-Type: application/json" -d '{"username": "joao.silva","password": "senha123","nome_completo": "João da Silva","cpf": "123.456.789-00"}'
curl -X POST http://localhost:8050/api/patients/register/ -H "Content-Type: application/json" -d '{ "username": "maria.silva", "password": "senha123", "nome_completo": "Maria da Silva", "cpf": "321.456.789-00" }'

Validar TOKEN
curl -X GET http://localhost:8050/api/patients/5e8c12a5-6353-4a72-96da-d6f77fd5310e/ -H "Authorization: Bearer seu-jwt-aqui"
curl -X GET http://localhost:8050/api/patients/fd1c0913-9139-4205-bb01-3e5cb9ae3d8f/ -H "Authorization: Bearer [seu-jwt-aqui]"

Autenticação
curl -X POST http://localhost:8050/api/auth/login/ -H "Content-Type: application/json" -d '{"username": "test", "password": "test"}'

Serviço de AI
curl -X POST http://localhost:8070/api/ai/chat -d '{"prompt": "O que é um prontuário médico?"}'
