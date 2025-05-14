from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, whatsapp, nome, password=None):
        if not whatsapp:
            raise ValueError("O campo WhatsApp é obrigatório")
        if not nome:
            raise ValueError("O campo Nome é obrigatório")

        user = self.model(nome=nome, whatsapp=whatsapp)
        user.save(using=self._db)
        return user

    def create_superuser(self, whatsapp, nome, password):
        user = self.create_user(whatsapp, nome, password)
        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    whatsapp = models.CharField(max_length=15, unique=True)
    nome = models.CharField(max_length=100)
    username = None
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    pontos = models.IntegerField(default=0)
    ultimo_endereco = models.TextField(null=True, blank=True)

    USERNAME_FIELD = 'whatsapp'  # Campo usado para login
    REQUIRED_FIELDS = ['nome']   # Campos obrigatórios ao criar o usuário

    objects = CustomUserManager()

    def __str__(self):
        return self.nome

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class Bairro(models.Model):
    nome= models.CharField(max_length=50, unique=True)
    taxa_entrega = models.DecimalField(max_digits=3, decimal_places=2)
    def __str__(self):
        return f'{self.nome} - R$ {self.taxa_entrega:.2f}'

class Categoria(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    descricao = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.nome
class Produto(models.Model):
    nome = models.CharField(max_length=30, unique=True, help_text="Nome do sabor da esfiha")
    descricao = models.TextField(blank=True, help_text="Descrição dos igredientes")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='produtos')
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    disponivel = models.BooleanField(default=True)
    imagem = models.ImageField(upload_to='imagens/',blank=True, null=True)
    trocavel_por_pontos = models.BooleanField(default=False)
    pontos_troca = models.DecimalField(max_digits=5, decimal_places=0)

    def __str__(self):
        return self.nome

class Pedido(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_preparo', 'Em preparo'),
        ('pronto', 'Pronto para retirada'),
        ('a_caminho', 'A caminho'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedidos')
    endereco = models.CharField(max_length=100, blank=True)
    itens = models.TextField(max_length=100)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    taxa_entrega = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    taxa_cartao = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    troco = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bairro = models.ForeignKey(Bairro, on_delete=models.CASCADE, null=True, related_name='bairro')
    forma_pagamento = models.CharField(max_length=20, blank=True)
    pago = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pendente')
    pontos_ganhos = models.DecimalField(max_digits=20, decimal_places=0, blank=True)
    def __str__(self):
        return f'Pedido {self.id} - {self.user.nome}'



class ConfiguracaoLoja(models.Model):
    loja_aberta = models.BooleanField(default=True)
    mensagem_fechada = models.TextField(default="Estamos fechados no momento.")
    imagem_fechada = models.ImageField(upload_to='imagens/loja/', blank=True, null=True)

    def __str__(self):
        return "Configuração da Loja"