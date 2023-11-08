
from django.contrib import admin
from django.urls import path, include, re_path
from django.shortcuts import redirect

from django.conf import settings
from django.conf.urls.static import static

def redirect_to_auth(request):
    return redirect('/auth/autentica/')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('usuarios.urls')),
    path('producao/', include('producao_cientifica.urls')),
    path('publicacoes/', include('producao_cientifica.urls')),
    path('', redirect_to_auth),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)