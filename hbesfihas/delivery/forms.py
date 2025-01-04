from django import forms
from .models import Pedido, Itens

class EntradaForm(forms.Form):
    nome = forms.CharField(
        max_length=50,
        required=True, 
        label="Nome",
        widget=forms.TextInput(attrs={'placeholder': 'Digite seu nome'})
    )
    whatsapp = forms.CharField(
        max_length=15,
        required=True, 
        label='WhatsApp',
        widget=forms.TextInput(attrs={'placeholder': 'Digite seu WhatsApp'})
    )

class LoginForm(forms.ModelForm):
    whatsapp = forms.CharField(max_length=15, label="Número do WhatsApp")
    nome = forms.CharField (max_length=100, label="Nome", required=True)

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['user', 'endereco', 'itens', 'subtotal', 'total','taxa_entrega', 'taxa_cartao','troco', 'bairro', 'forma_pagamento']
        widgets = {
            'bairro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Selecione o bairro'}),
            'forma_pagamento': forms.Select(attrs={'class': 'form-control'}),
            'endereco': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Informe o endereço'}),
        }

