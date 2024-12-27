from django import forms
from .models import Pedido, ItemPedido

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['bairro', 'forma_pagamento', 'endereco']
        widgets = {
            'bairro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Selecione o bairro'}),
            'forma_pagamento': forms.Select(attrs={'class': 'form-control'}),
            'endereco': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Informe o endereço'}),
        }

class ItemPedidoForm(forms.ModelForm):
    class Meta:
        model = ItemPedido
        fields = ['produto', 'quantidade']
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
