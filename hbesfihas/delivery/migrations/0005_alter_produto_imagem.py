# Generated by Django 5.1.4 on 2024-12-16 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("delivery", "0004_alter_pedido_cliente_alter_produto_imagem"),
    ]

    operations = [
        migrations.AlterField(
            model_name="produto",
            name="imagem",
            field=models.ImageField(blank=True, null=True, upload_to="produtos/"),
        ),
    ]
