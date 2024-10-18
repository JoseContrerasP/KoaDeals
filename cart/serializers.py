from rest_framework import serializers
from item.models import Item
from .models import Pedido, Cart

# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Item
#         fields = "__all__"

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = ["id", "item", "owner", "item_price", "quantity", "get_total_pedido"]

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["id", "pedido", ]