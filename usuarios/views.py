from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm 

def autentica(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        username = request.POST.get('username')
        email = request.POST.get('email')
        if User.objects.filter(username=username).exists():
            form.add_error('username', 'Usuário já cadastrado!')
        if User.objects.filter(email=email).exists():
            form.add_error('email', 'E-mail já cadastrado!')
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário cadastrado com sucesso!')
            return render(request, 'autentica.html', {'form': form}) 
    else:
        form = CustomUserCreationForm()
    return render(request, 'autentica.html', {'form': form})


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Usuário ou senha incorretos.')
            return redirect('login')
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')