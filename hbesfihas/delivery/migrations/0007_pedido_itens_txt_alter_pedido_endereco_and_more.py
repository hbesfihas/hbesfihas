# Generated by Django 5.1.4 on 2025-01-02 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0006_remove_pedido_taxa_cartao_credito_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='itens_txt',
            field=models.TextField(default=0, max_length=500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pedido',
            name='endereco',
            field=models.TextField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='forma_pagamento',
            field=models.CharField(max_length=20),
        ),
    ]