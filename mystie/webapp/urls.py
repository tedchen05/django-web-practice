from django.urls import path

from .views import menu, cart, home, invoice

urlpatterns = [
    path('home', home.home, name='home'),
    path('menu', menu.menu, name='menu'),
    path('cart', cart.cart, name='cart'),
    path('invoice', invoice.invoice, name='invoice'),
    path('invoice_login', invoice.invoice_login, name='invoice_login'),
    path('order-product', cart.order_product, name='order_product'),
    path('cart-update', cart.cart_update, name='cart_update'),
    path('cart-remove', cart.cart_remove, name='cart_remove'),

]