# Exemplo de uso no seu código Python
from patients.models import Patient

novo_paciente = Patient(nome_completo='Ana Silva', cpf='123.456.789-00')
novo_paciente.save() # O ORM traduzirá isso para um comando SQL INSERT