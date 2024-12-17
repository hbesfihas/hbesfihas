from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=100, null=True)
    whatsapp = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return f"{self.nome} ({self.whatsapp})"
    
class Produto(models.Model):
    nome = models.CharField(max_length=30, unique=True, help_text="Nome do sabor da esfiha")
    descricao = models.TextField(blank=True, help_text="Descrição dos igredientes")
    preco = models.DecimalField(max_digits=3, decimal_places=2)
    imagem = models.ImageField(upload_to='produtos/',blank=True, null=True)
    
    def __str__(self):
        return self.nome
    
class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True)
    bairro = models.CharField(max_length=50)
    endereco = models.TextField(blank=True, null=True)
    forma_pagamento = models.CharField(max_length=20, blank=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Pedido {self.id} - {self.cliente.nome}'


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