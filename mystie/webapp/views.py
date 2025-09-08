import json

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render

from webapp.models import Product, Navigation, OrderProduct


# Create your views here.

@login_required(login_url='/')
def menu(request):
    products = Product.objects.all()
    nav_items = Navigation.objects.all().order_by('order')
    data = {'products': products, 'nav_items': nav_items}
    return render(request, 'webapp/menu.html', data)

@login_required(login_url='/')
def cart(request):
    order_products = OrderProduct.objects.filter(customer=request.user)
    nav_items = Navigation.objects.all().order_by('order')
    total_amount = order_products.aggregate(Sum('total_price'))['total_price__sum'] or 0

    context = {
        'order_products': order_products,
        'nav_items': nav_items,
        'total_amount': total_amount
    }
    return render(request, 'webapp/cart.html', context)

@login_required(login_url='/')
def cart_update(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_quantity = int(data.get('quantity'))
        item_id = data.get('item_id')

        item = OrderProduct.objects.get(id=item_id)
        product = Product.objects.get(name=item.product_name)
        product_price = product.price

        item.quantity = new_quantity
        item.total_price = product_price * new_quantity
        item.save()

        total_amount = OrderProduct.objects.filter(customer=request.user).aggregate(Sum('total_price'))['total_price__sum'] or 0

        return JsonResponse({'status': 'success', 'new_quantity': item.quantity, 'new_total_price': item.total_price, 'order_total': round(total_amount, 2)})
    return JsonResponse({'status': 'error', 'message': '只接受 POST 請求'}, status=405)

@login_required(login_url='/')
def home(request):
    nav_items = Navigation.objects.all().order_by('order')
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
            price =product.price,
            total_price=total_price
        )
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


