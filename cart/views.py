import requests
from django.shortcuts import render, redirect

from rest_framework.views import APIView
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from item.models import Item as Product

from .serializers import PedidoSerializer, CartSerializer 
from .models import Pedido, Cart

# Import PayPal stuff
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid # unique user id for duplicate orders


class CartAPIView(generics.CreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        pedidos = Pedido.objects.filter(owner=request.user)

        total = 0
        quantities = 0
        for pedido in pedidos:        
            total += pedido.get_total_pedido()
            quantities += pedido.quantity

        host = request.get_host()

        if settings.DEBUG:
            paypal_dict = {
                "business": settings.PAYPAL_RECEIVER_EMAIL,
                "amount": total,
                "item_name": "Item Name", # later we can make it more precise
                "no_shipping": "2",
                "invoice": str(uuid.uuid4()),
                "currency_code": "USD",
                "notify_url": f"http://{host}{reverse("paypal-ipn")}",
                "return_url": f"http://{host}{reverse("core:payment_success")}",
                "cancel_return": f"http://{host}{reverse("core:payment_failed")}",
            }

        else:
            paypal_dict = {
                "business": settings.PAYPAL_RECEIVER_EMAIL,
                "amount": total,
                "item_name": "Item Name", # later we can make it more precise
                "no_shipping": "2",
                "invoice": str(uuid.uuid4()),
                "currency_code": "USD",
                "notify_url": f"https://{host}{reverse("paypal-ipn")}",
                "return_url": f"https://{host}{reverse("core:payment_success")}",
                "cancel_return": f"https://{host}{reverse("core:payment_failed")}",
            }

        paypal_form = PayPalPaymentsForm(initial=paypal_dict)

        context = {"pedidos": pedidos, "total": total, "quantities": quantities, "paypal_form": paypal_form}
        return render(request, "cart/cart.html", context)

    def post(self, request, *args, **kwargs):
        if settings.DEBUG:
            default_endpoint = settings.LOCAL_ENDPOINT
        else:
            default_endpoint = settings.DEPLOY_ENDPOINT

        endpoint = default_endpoint + "pedido/"

        if "delete" in request.POST:
            pedido_id = request.POST.get("delete")
            endpoint += pedido_id + "/"
            request_delete = requests.delete(endpoint)
            
        elif "add" in request.POST:
            pedido_id = request.POST.get("add")
            endpoint += pedido_id + "/"
            pedido = Pedido.objects.get(pk=pedido_id)
            new_quantity = pedido.quantity + 1
            data = {
                "quantity": new_quantity
            }
            request_patch = requests.patch(endpoint, json=data)

        elif "subtract" in request.POST:
            pedido_id = request.POST.get("subtract")
            endpoint += pedido_id + "/"
            pedido = Pedido.objects.get(pk=pedido_id)
            new_quantity = pedido.quantity - 1
            data = {
                "quantity": new_quantity
            }
            request_patch = requests.patch(endpoint, json=data)

        else:
            return self.create(request, *args, **kwargs)

        return redirect("cart:cart")

class PedidoAPIView(generics.ListCreateAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    # permission_classes = [permissions.IsAuthenticated]

class PedidoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    # permission_classes = [permissions.IsAuthenticated]

class CartRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    # permission_classes = [permissions.IsAuthenticated]


