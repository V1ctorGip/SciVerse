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
        # Atualiza campos existentes
        profile.full_name = request.POST.get('full_name', profile.full_name)
        profile.email = request.POST.get('email', profile.email)
        profile.phone = request.POST.get('phone', profile.phone)
        profile.course = request.POST.get('course', profile.course)
        profile.bio = request.POST.get('bio', profile.bio)
        profile.linkedin_url = request.POST.get('linkedin_url', profile.linkedin_url)
        profile.github_url = request.POST.get('github_url', profile.github_url)
        profile.instagram_url = request.POST.get('instagram_url', profile.instagram_url)

        # Adiciona lógica para lidar com o upload de imagens
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']

        profile.save()

    form = UserProfileForm(instance=profile)
    return render(request, 'perfil.html', {'form': form})
