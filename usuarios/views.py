from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm 
from .models import UserProfile
from .forms import UserProfileForm 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver


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

from .models import UserProfile
from .forms import UserProfileForm # você precisará criar este formulário


@login_required
def perfil(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile.bio = form.cleaned_data.get('bio')  # Garantir que a bio seja atualizada
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('perfil')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'perfil.html', {'form': form})
