from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    # path('products/', views.ProductAPI.as_view(), name='products'),
    path('cart/', views.CartAPIView.as_view(), name='cart'),
    path('pedido/', views.PedidoAPIView.as_view(), name='pedido'),
    path('pedido/<int:pk>/', views.PedidoRetrieveUpdateDestroyAPIView.as_view(), name='pedido_rest'),
    path('cart/<int:pk>/', views.CartRetrieveUpdateDestroyAPIView.as_view(), name='cart_rest'),
]