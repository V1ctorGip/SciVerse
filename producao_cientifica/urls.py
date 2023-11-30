from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('orientadores/', views.lista_orientadores, name='lista_orientadores'), 
    path('publicacoes/', views.lista_de_publicacoes, name='lista_de_publicacoes'),
    path('orientadores/ajax_search', views.ajax_search, name='ajax_search'),
    path('publicacoes/ajax_search_publicacoes', views.ajax_search_publicacoes, name='ajax_search_publicacoes'),
    path('producao-cientifica/por-curso/', views.producao_cientifica_por_curso, name='api-producao-cientifica-por-curso'),
    path('producao-cientifica/por-ano/', views.producao_cientifica_por_ano, name='api-producao-por-ano'),
    path('producao-cientifica/top-orientadores/', views.top_orientadores, name='api-top-orientadores'),
    path('producao-cientifica/palavras-chave-emergentes/', views.palavras_chave_emergentes_por_ano, name='api-palavras-chave-emergentes'),
    path('orientadores/perfil/<str:nome_orientador>/', views.perfil_orientador, name='perfil_orientador'),
    path('producao-cientifica/orientador/<str:orientador>/', views.producao_cientifica_orientador, name='api-producao-cientifica-orientador'),
    path('producao-cientifica/top-orientadores-comparativo/', views.top_orientadores_comparativo, name='top-orientadores-comparativo'),
    path('producao-cientifica/orientacoes-por-curso/<str:nome_orientador>/', views.orientacoes_por_curso, name='api-orientacoes-por-curso'),
    path('producao-cientifica/palavras-chave-orientador/<str:orientador>/', views.palavras_chave_orientador, name='palavras-chave-orientador'),
    path('producao-cientifica/top-multidisciplinar/', views.top_orientadores_multidisciplinar, name='top-multidisciplinar'),
]




