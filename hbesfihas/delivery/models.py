from django.db import models
class Bairro(models.Model):
    nome= models.CharField(max_length=50, unique=True)
    taxa_entrega = models.DecimalField(max_digits=3, decimal_places=2)
    def __str__(self):
        return f'{self.nome} - R$ {self.taxa_entrega:.2f}'


class Cliente(models.Model):
    nome = models.CharField(max_length=100, null=True)
    whatsapp = models.CharField(max_length=15, unique=True)
    endereco = models.TextField(null=True)

    def __str__(self):
        return f"{self.nome} ({self.whatsapp})"
    
class Produto(models.Model):
    nome = models.CharField(max_length=30, unique=True, help_text="Nome do sabor da esfiha")
    descricao = models.TextField(blank=True, help_text="Descrição dos igredientes")
    preco = models.DecimalField(max_digits=3, decimal_places=2)
    imagem = models.ImageField(upload_to='imagens/',blank=True, null=True)
    
    def __str__(self):
        return self.nome
    
class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True)
    bairro = models.ForeignKey(Bairro, on_delete=models.SET_NULL, null=True)
    endereco = models.TextField(blank=True, null=True)
    localizacao = models.CharField(max_length=20, blank=True)
    forma_pagamento = models.CharField(max_length=20, blank=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Pedido {self.id} - {self.cliente.nome}'

    def calcular_total(self):
        total_itens = sum(item.calcular_subtotal() for item in self.itens.all())
        taxa_entrega = self.bairro.taxa_entrega if self.bairro else 0
        self.valor_total = total_itens + taxa_entrega
        self.save()
        return self.valor_total

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=8, decimal_places=2)  # Capturado do Produto

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} (Pedido {self.pedido.id})"

    # Método para calcular o subtotal do item
    def calcular_subtotal(self):
        return self.quantidade * self.preco_unitario
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.pedido.calcular_total()

