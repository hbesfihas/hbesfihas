# Generated by Django 5.1.4 on 2025-01-03 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0009_alter_pedido_bairro'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedido',
            name='itens',
        ),
        migrations.AddField(
            model_name='pedido',
            name='itens',
            field=models.TextField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]