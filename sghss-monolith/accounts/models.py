# Create your models here.
# sghss-monolith/accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    """
    Representa o papel de um usuário no sistema (ex: Paciente, Médico).
    """
    nome = models.CharField(max_length=50, unique=True, null=False)

    def __str__(self):
        return self.nome

class User(AbstractUser):
    """
    Representa o usuário base do sistema, herdando campos do Django.
    """
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username