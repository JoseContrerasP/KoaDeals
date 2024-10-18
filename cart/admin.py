from django.contrib import admin

# from .models import Product
from .models import Pedido, Cart

admin.site.register(Cart)
admin.site.register(Pedido)
