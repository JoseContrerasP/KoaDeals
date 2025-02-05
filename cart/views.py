import requests
from django.shortcuts import render, redirect
from django.conf import settings

from rest_framework.views import APIView
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from item.models import Item as Product

from .serializers import PedidoSerializer, CartSerializer 
from .models import Pedido, Cart

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

        context = {"pedidos": pedidos, "total": total, "quantities": quantities}
        return render(request, "cart/cart.html", context)

    def post(self, request, *args, **kwargs):
        
        if settings.DEBUG:
            default_endpoint = "http://localhost:8000/"
        else:
            default_endpoint = "http://127.0.0.1:8000/"

        endpoint = default_endpoint + "pedido/"
        
        if "delete" in request.POST:
            pedido_id = request.POST.get("delete")
            endpoint += pedido_id + "/"
            request_delete = requests.delete(endpoint)
            return redirect("cart:cart")

        elif "add" in request.POST:
            pedido_id = request.POST.get("add")
            endpoint += pedido_id + "/"
            pedido = Pedido.objects.get(pk=pedido_id)
            new_quantity = pedido.quantity + 1
            data = {
                "quantity": new_quantity
            }
            request_patch = requests.patch(endpoint, json=data)
            return redirect("cart:cart")

        elif "subtract" in request.POST:
            pedido_id = request.POST.get("subtract")
            endpoint += pedido_id + "/"
            pedido = Pedido.objects.get(pk=pedido_id)
            new_quantity = pedido.quantity - 1
            data = {
                "quantity": new_quantity
            }
            request_patch = requests.patch(endpoint, json=data)
            return redirect("cart:cart")

        else:
            return self.create(request, *args, **kwargs)

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


