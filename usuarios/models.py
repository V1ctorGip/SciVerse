# producao_cientifica/models.py
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

class Autor(models.Model):
    TIPO_CHOICES = [
        ('Principal', 'Principal'),
        
    ]
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    nome = models.CharField(max_length=255)

class ProducaoCientifica(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    titulo = models.CharField(max_length=255)
    nome_do_curso = models.CharField(max_length=255)
    nome_orientador = models.CharField(max_length=255)
    link_arquivo = models.URLField()
    autores = models.ManyToManyField(Autor)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField("Bio", blank=True)
    full_name = models.CharField("Full Name", max_length=255, blank=True)
    email = models.EmailField("Email", blank=True)
    phone = models.CharField("Phone", max_length=20, blank=True)
    course = models.CharField("Course", max_length=255, blank=True)
    instagram_url = models.URLField("Instagram URL", blank=True)
    github_url = models.URLField("GitHub URL", blank=True)
    website_url = models.URLField("Website URL", blank=True)
    profile_picture = models.ImageField("Profile Picture", upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('user_profile', kwargs={'username': self.user.username})
