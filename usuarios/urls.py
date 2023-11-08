from django.urls import path
from . import views

urlpatterns = [
    path('autentica/', views.autentica, name='autentica'),
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    
]