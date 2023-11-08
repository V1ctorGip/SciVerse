from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('orientadores/', views.lista_orientadores, name='lista_orientadores'), 
    path('publicacoes/', views.lista_de_publicacoes, name='lista_de_publicacoes'),
    path('orientadores/ajax_search', views.ajax_search, name='ajax_search'),
    path('publicacoes/ajax_search_publicacoes', views.ajax_search_publicacoes, name='ajax_search_publicacoes'),
   
]


