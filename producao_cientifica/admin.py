from django.contrib import admin
from .models import ProducaoCientifica, Autor

class ProducaoCientificaAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'nome_do_curso', 'nome_orientador', 'link_arquivo', 'get_autores')

    def get_autores(self, obj):
        return ", ".join([autor.nome for autor in obj.autores.all()])
    get_autores.short_description = 'Autores'

admin.site.register(ProducaoCientifica, ProducaoCientificaAdmin)
