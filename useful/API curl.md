Registrar Paciente
curl -X POST http://localhost:8050/api/patients/register/ -H "Content-Type: application/json" -d '{"username": "joao.silva","password": "senha123","nome_completo": "João da Silva","cpf": "123.456.789-00"}'
curl -X POST http://localhost:8050/api/patients/register/ -H "Content-Type: application/json" -d '{ "username": "maria.silva", "password": "senha123", "nome_completo": "Maria da Silva", "cpf": "321.456.789-00" }'

Validar TOKEN
curl -X GET http://localhost:8050/api/patients/5e8c12a5-6353-4a72-96da-d6f77fd5310e/ -H "Authorization: Bearer seu-jwt-aqui"

curl -X GET http://localhost:8050/api/patients/fd1c0913-9139-4205-bb01-3e5cb9ae3d8f/ -H "Authorization: Bearer [seu-jwt-aqui]"

curl -X GET http://localhost:8050/api/patients/fec052b2-b303-4d6a-b9e2-59c28ccb4d29/ -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZmVjMDUyYjItYjMwMy00ZDZhLWI5ZTItNTljMjhjY2I0ZDI5IiwiZXhwIjoxNzYwMzI1OTM2LCJpYXQiOjE3NjAzMjIzMzZ9.O9ozxc9rTQEVKFyUopQ6GMOM5Hrn-WeipIBbEZWc7YA"

curl -X GET http://localhost:8060/api/auth/validate -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZmVjMDUyYjItYjMwMy00ZDZhLWI5ZTItNTljMjhjY2I0ZDI5IiwiZXhwIjoxNzYwMzI1OTM2LCJpYXQiOjE3NjAzMjIzMzZ9.O9ozxc9rTQEVKFyUopQ6GMOM5Hrn-WeipIBbEZWc7YA"


Login de Autenticação
curl -X POST http://localhost:8050/api/auth/login/ -H "Content-Type: application/json" -d '{"username": "test", "password": "testpassword"}'

curl -X POST http://localhost:8050/api/auth/login/ -H "Content-Type: application/json" -d '{"username": "test.user.17603220", "password": "testpassword"}'

# Serviço de AI
## Java - Spring Boot
curl -X POST http://localhost:8080/api/v1/ai-proxy/chat -H "Content-Type: application/json" -d '{"prompt": "Quais são as regras de privacidade de dados em hospitais?"}'

## Python - Flask
curl -X POST http://localhost:8070/api/ai/chat -H "Content-Type: application/json" -d '{"prompt": "O que é um prontuário médico?"}'

curl -X POST http://localhost:8070/api/ai/chat -d '{"prompt": "O que é um prontuário médico?"}'



id
abeb8432-4669-4d82-912c-a59e6a527d81
Paciente Teste 17602779
Paciente.Teste.17602779
test.user.17602779

fec052b2-b303-4d6a-b9e2-59c28ccb4d29
test.user.17603220
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZmVjMDUyYjItYjMwMy00ZDZhLWI5ZTItNTljMjhjY2I0ZDI5IiwiZXhwIjoxNzYwMzI1OTM2LCJpYXQiOjE3NjAzMjIzMzZ9.O9ozxc9rTQEVKFyUopQ6GMOM5Hrn-WeipIBbEZWc7YA