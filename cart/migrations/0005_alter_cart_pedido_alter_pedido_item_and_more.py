# Generated by Django 4.2.5 on 2024-10-20 16:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("item", "0003_alter_item_image"),
        ("cart", "0004_alter_cart_created_at_remove_cart_pedido_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="pedido",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="carts",
                to="cart.pedido",
            ),
        ),
        migrations.AlterField(
            model_name="pedido",
            name="item",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="item.item",
            ),
        ),
        migrations.AlterField(
            model_name="pedido",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="pedidos",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="pedido",
            name="quantity",
            field=models.PositiveSmallIntegerField(),
        ),
    ]
