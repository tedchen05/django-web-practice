from django.urls import path

from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('menu', views.menu, name='menu'),
    path('cart', views.cart, name='cart'),
    path('order-product', views.order_product, name='order_product'),
    path('cart-update', views.cart_update, name='cart_update'),
]