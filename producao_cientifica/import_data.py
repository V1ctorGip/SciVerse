import sys
sys.path.append('C:\\Users\\Victor\\Desktop\\Teste com Django')

import os
import django
import json
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dash.settings')
django.setup()

from producao_cientifica.models import ProducaoCientifica, Autor, PalavraChave

def import_data_from_json():
    with open('dados_normalizados_consolidados.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        
        for item in data:
            producao = ProducaoCientifica(
                id=item['Id'],
                titulo=item['Titulo'],
                data_da_defesa=datetime.strptime(item['DataDaDefesa'], '%Y-%m-%d').date(),
                nome_do_curso=item['NomeDoCurso'],
                nome_orientador=item['NomeOrientador'],
                link_arquivo=item['LinkArquivo']
            )
            producao.save()

            for autor_data in item['Autores']:
                autor, created = Autor.objects.get_or_create(
                    tipo=autor_data['Tipo'],
                    nome=autor_data['Nome']
                )
                producao.autores.add(autor)

            for palavra_data in item['PalavrasChave']:
                palavra_chave, created = PalavraChave.objects.get_or_create(
                    termo=palavra_data['Termo']
                )
                producao.palavras_chave.add(palavra_chave)

            print(f"Produção {producao.titulo} importada com sucesso!")

if __name__ == '__main__':
    import_data_from_json()
