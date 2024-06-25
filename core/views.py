from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


@login_required
def logout_session(request):
    logout(request)
    return redirect('index')

def index(request):
    return render(request, 'index.html', {})

@login_required
def home(request):
    return render(request, 'home.html', {})