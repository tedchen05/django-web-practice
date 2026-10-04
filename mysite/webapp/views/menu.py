from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from webapp.models import Product
from webapp.views.home import get_navigation


# Create your views here.

@login_required(login_url='/')
def menu(request):
    products = Product.objects.all()
    # nav_items = Navigation.objects.all().order_by('order')
    nav_items = get_navigation()
    data = {'products': products, 'nav_items': nav_items}
    return render(request, 'webapp/menu.html', data)

