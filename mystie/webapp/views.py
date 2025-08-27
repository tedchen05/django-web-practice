import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from webapp.models import Product, Navigation, OrderProduct


# Create your views here.

@login_required(login_url='/')
def menu(request):
    products = Product.objects.all()
    nav_items = Navigation.objects.all()
    data = {'products': products, 'nav_items': nav_items}
    return render(request, 'webapp/menu.html', data)

@login_required(login_url='/')
def cart(request):
    order_products = OrderProduct.objects.filter(customer=request.user)
    nav_items = Navigation.objects.all()
    context = {
        'order_products': order_products,
        'nav_items': nav_items
    }
    return render(request, 'webapp/cart.html', context)

@login_required(login_url='/')
def home(request):
    nav_items = Navigation.objects.all()
    return render(request, 'webapp/base.html', {'nav_items': nav_items})

@login_required(login_url='/')
def order_product(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))

        product = Product.objects.get(id=product_id)
        total_price = product.price * quantity

        OrderProduct.objects.create(
            product_name=product.name,
            customer=request.user,
            quantity=quantity,
            total_price=total_price
        )
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


