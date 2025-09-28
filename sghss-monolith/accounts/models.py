# Create your models here.
# sghss-monolith/accounts/models.py
"""
A regra de nomenclatura do Django para tabelas do banco de dados é a seguinte:

Nome da Tabela=nome_da_app_nome_da_classe_do_modelo

para cada classe dentro de Models, será criado uma nova tabela

accounts_Role
accounts_CustomUserManager
accounts_User
accounts_Permission 

"""


from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import uuid

class Role(models.Model):
    """
    Representa o papel de um usuário no sistema (ex: Paciente, Médico).
    """
    nome = models.CharField(max_length=50, unique=True, null=False)

    def __str__(self):
        return self.nome

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True)

    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    #Criados para não dar mais erro de campo nulo.
    #first_name = models.CharField(max_length=150, blank=True)
    #last_name = models.CharField(max_length=150, blank=True)
    #email = models.EmailField(blank=True)
    

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    """
        SCHEMA da tabela que é gerada automaticamente no banco de dado.
        Só por utilizar o AbstractBaseUser ele cria automaticamente os campos com * na frente
            
            Column    |           Type           | Collation | Nullable | Default 
        --------------+--------------------------+-----------+----------+---------
        password     | character varying(128)   |           | not null | 
        *last_login   | timestamp with time zone |           |          | 
        *is_superuser | boolean                  |           | not null | 
        username     | character varying(150)   |           | not null | 
        *first_name   | character varying(150)   |           | not null | 
        *last_name    | character varying(150)   |           | not null | 
        *email        | character varying(254)   |           | not null | 
        is_staff     | boolean                  |           | not null | 
        is_active    | boolean                  |           | not null | 
        *date_joined  | timestamp with time zone |           | not null | 
        role_id      | bigint                   |           |          | 
        id           | uuid                     |           | not null | 

    """

    def __str__(self):
        return self.username

class Permission(models.Model):
    nome_acao = models.CharField(max_length=255, unique=True)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome_acao

class RolePermission(models.Model):
    #Tabela MUITOS para MUITOS
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        """ CLASSE ANINHADA - REGRA D RESTRIÇÃO COMPOSTA
        Primary Key Compost
        Reflexo no Banco de Dados:
            O Django cria uma restrição ou índice único no banco de dados que impede que a mesma Role tenha a mesma Permission registrada mais de uma vez.
            Por exemplo, a combinação (Administrador, Ler Relatórios) só pode existir uma vez.
        """
        unique_together = ('role', 'permission')

    def __str__(self):
        return f"{self.role.nome} tem permissão para {self.permission.nome_acao}"