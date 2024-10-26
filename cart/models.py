from django.db import models
from django.contrib.auth.models import User
from item.models import Item



# from django.db import models

# class Product(models.Model):
#     name = models.CharField(max_length=150)
#     description = models.TextField(blank=True)
    # price = models.DecimalField(max_digits=10, decimal_places=2)
#     image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
#     is_available = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     modified_at = models.DateTimeField(auto_now=True)

#     def __str__(self) -> str:
#         return str(self.name)

class Pedido(models.Model):
	item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True, null=True)
	owner = models.ForeignKey(User, related_name="pedidos", on_delete=models.CASCADE, blank=True, null=True)

	quantity = models.PositiveSmallIntegerField()

	created_at = models.DateTimeField(auto_now_add=True)

	def get_total_pedido(self):
		return self.quantity * self.item.price

	def item_price(self):
		return self.item.price

	def __str__(self):
		return f"{self.item.name} - {self.quantity}"

class Cart(models.Model):
	pedido = models.ForeignKey(Pedido, related_name="carts", on_delete=models.CASCADE, blank=True, null=True)

	modified_at = models.DateTimeField(auto_now=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def get_total(self):
		return self.pedido.get_total_pedido()

	def __str__(self):
		return f"{self.pedido.owner}"