from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
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


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    endereco = models.CharField(max_length=255)
    bairro = models.ForeignKey(Bairro, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Perfil de {self.user.nome} - {self.user.whatsapp}"
    
class Produto(models.Model):
    nome = models.CharField(max_length=30, unique=True, help_text="Nome do sabor da esfiha")
    descricao = models.TextField(blank=True, help_text="Descrição dos igredientes")
    preco = models.DecimalField(max_digits=3, decimal_places=2)
    imagem = models.ImageField(upload_to='imagens/',blank=True, null=True)
    
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
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pendente')

    def __str__(self):
        return f'Pedido {self.id} - {self.user.nome}'


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} (Pedido {self.pedido.id})"
 
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.pedido.calcular_total()

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Cria o perfil do usuário quando o usuário é criado
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    # Salva o perfil do usuário sempre que o usuário for salvo
    instance.profile.save()
