from rest_framework import serializers
from .models import Produto, Pedido, ItemPedido, Cliente


class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ['id', 'nome', 'descricao', 'preco', 'imagem']



class ItemPedidoSerializer(serializers.ModelSerializer):
    produto = ProdutoSerializer()

    class Meta: 
        model = ItemPedido
        fields = ['produto', 'quantidade', 'preco_unitario', 'calcular_subtotal']

    calcular_subtotal = serializers.SerializerMethodField()

    def get_calcular_subtotal(self, obj):
        return obj.calcular_subtotal()
    

class PedidoSerializer(serializers.ModelSerializer):
    itens = ItemPedidoSerializer(many=True)
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    cliente_whatsapp = serializers.CharField(source='cliente.whatsapp', read_only=True)

    class Meta:
        model = Pedido
        fields = [
            'id', 'cliente_nome', 'cliente_whatsapp', 'bairro',
            'endereco', 'forma_pagamento', 'valor_total', 'itens', 'criado_em'
        ]

class PedidoCreateSerializer(serializers.ModelSerializer):
    itens = serializers.ListField(write_only=True)

    class Meta:
        model = Pedido
        fields = ['cliente', 'bairro', 'endereco', 'forema_pagamento', 'itens']

        def create(self, validated_data):
            itens_data = validated_data.pop('itens')
            pedido = Pedido.objects.create(**validated_data)

            for item_data in itens_data:
                produto = Produto.objects.get(id=item_data['produto_id'])
                ItemPedido.objects.create(
                    pedido = pedido, 
                    produto = produto, 
                    quantidade = item_data['quantidade'], 
                    preco_unitario = produto.preco
                )
            pedido.calcular_total()
            return pedido