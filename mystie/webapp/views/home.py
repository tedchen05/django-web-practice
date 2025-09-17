from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from webapp.models import Navigation
from webapp.utils.home import get_navigation


# Create your views here.
# @login_required(login_url='/')
# def home(request):
#     nav_items = Navigation.objects.all().order_by('order')
#     return render(request, 'webapp/home.html', {'nav_items': nav_items})

@login_required(login_url='/')
def home(request):
    nav_items = get_navigation()
    return render(request, "webapp/home.html", {"nav_items": nav_items})


