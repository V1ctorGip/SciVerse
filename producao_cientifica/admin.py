from django.contrib import admin
from .models import ProducaoCientifica, Autor, PalavraChave

class ProducaoCientificaAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'data_da_defesa', 'nome_do_curso', 'nome_orientador', 'link_arquivo', 'get_autores', 'get_palavras_chave')

    def get_autores(self, obj):
        return ", ".join([autor.nome for autor in obj.autores.all()])
    get_autores.short_description = 'Autores'

    def get_palavras_chave(self, obj):
        return ", ".join([palavra_chave.termo for palavra_chave in obj.palavras_chave.all()])
    get_palavras_chave.short_description = 'Palavras-Chave'

admin.site.register(ProducaoCientifica, ProducaoCientificaAdmin)
