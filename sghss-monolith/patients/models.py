
# sghss-monolith/patients/models.py

from django.db import models
from accounts.models import User

class Patient(models.Model):
    """
    Representa os dados específicos de um paciente, com uma relação 1-para-1 com o User.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nome_completo = models.CharField(max_length=255, null=False)
    cpf = models.CharField(max_length=14, unique=True, null=False)
    data_nascimento = models.DateField(null=True, blank=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.nome_completo