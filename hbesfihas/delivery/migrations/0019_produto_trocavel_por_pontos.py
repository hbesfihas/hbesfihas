# Generated by Django 5.1.4 on 2025-01-21 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0018_pedido_pontos_ganhos'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='trocavel_por_pontos',
            field=models.BooleanField(default=False),
        ),
    ]
