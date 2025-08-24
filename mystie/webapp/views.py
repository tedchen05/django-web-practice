from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from webapp.models import Product, Navigation


# Create your views here.

@login_required(login_url='/')
def menu(request):
    products = Product.objects.all()
    nav_items = Navigation.objects.all()
    data = {'products': products, 'nav_items': nav_items}
    return render(request, 'webapp/menu.html', data)

@login_required(login_url='/')
def home(request):
    nav_items = Navigation.objects.all()
    return render(request, 'webapp/base.html', {'nav_items': nav_items})