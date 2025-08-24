from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


# Create your views here.
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # 已登入就導向首頁

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')  # 登入成功後導向首頁
        else:
            return render(request, 'accounts/login.html', {'form': {'errors': True}})
    return render(request, 'accounts/login.html')

def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('login')  # 登出後導向登入頁