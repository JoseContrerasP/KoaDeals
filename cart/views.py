import requests
from django.shortcuts import render, redirect

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
        # endpoint = "http://127.0.0.1:8000/pedido/"
        endpoint = "https://koa-deals.onrender.com/pedido/"
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
            print(request)
            return self.create(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     print(request.POST)
    #     print("action" in request.POST)
    #     return render(request, "core/contact.html")

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


# from .service import Cart

# class ProductAPI_false(APIView):
#     """
#     Single API to handle product operations
#     """
#     serializer_class = ProductSerializer

#     def get(self, request, format=None):
#         qs = Product.objects.all()

#         return Response(
#             {"data": self.serializer_class(qs, many=True).data}, 
#             status=status.HTTP_200_OK
#             )

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(
#             serializer.data, 
#             status=status.HTTP_201_CREATED
#             )

# class CartAPI_false(APIView):
#     """
#     Single API to handle cart operations
#     """
#     def get(self, request, format=None):
#         cart = Cart(request)

#         return Response(
#             {"data": list(cart.__iter__()), 
#             "cart_total_price": cart.get_total_price()},
#             status=status.HTTP_200_OK
#             )

#     def post(self, request, **kwargs):
#         cart = Cart(request)

#         if "remove" in request.data:
#             product = request.data["product"]
#             cart.remove(product)

#         elif "clear" in request.data:
#             cart.clear()

#         else:
#             product = request.data
#             cart.add(
#                     product=product["product"],
#                     quantity=product["quantity"],
#                     overide_quantity=product["overide_quantity"] if "overide_quantity" in product else False
#                 )
#             print(request.data)

#         return Response(
#             {"message": "cart updated"},
#             status=status.HTTP_202_ACCEPTED
#         )
