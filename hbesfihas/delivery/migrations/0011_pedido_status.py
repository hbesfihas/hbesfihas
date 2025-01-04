# Generated by Django 5.1.4 on 2025-01-04 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0010_remove_pedido_itens_pedido_itens'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='status',
            field=models.CharField(choices=[('pendente', 'Pendente'), ('em_preparo', 'Em preparo'), ('pronto', 'Pronto para retirada'), ('a_caminho', 'A caminho'), ('entregue', 'Entregue'), ('cancelado', 'Cancelado')], default='pendente', max_length=15),
        ),
    ]