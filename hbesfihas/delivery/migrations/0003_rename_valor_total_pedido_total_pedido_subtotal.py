# Generated by Django 5.1.4 on 2024-12-30 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("delivery", "0002_rename_cliente_pedido_user"),
    ]

    operations = [
        migrations.RenameField(
            model_name="pedido",
            old_name="valor_total",
            new_name="total",
        ),
        migrations.AddField(
            model_name="pedido",
            name="subtotal",
            field=models.DecimalField(
                blank=True, decimal_places=2, default=0, max_digits=8
            ),
            preserve_default=False,
        ),
    ]
