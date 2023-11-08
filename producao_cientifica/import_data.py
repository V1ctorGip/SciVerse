import sys
sys.path.append('C:\\Users\\Victor\\Desktop\\Teste com Django')

import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dash.settings')
django.setup()

from producao_cientifica.models import ProducaoCientifica, Autor


def import_data_from_json():
    with open('dados_normalizados_consolidados.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        
        for item in data:
            producao = ProducaoCientifica(
                id=item['Id'],
                titulo=item['Titulo'],
                nome_do_curso=item['NomeDoCurso'],
                nome_orientador=item['NomeOrientador'],
                link_arquivo=item['LinkArquivo']
            )
            producao.save()
            print(f"Produção {producao.titulo} importada com sucesso!")

            
            for autor_data in item['Autores']:
                autor, created = Autor.objects.get_or_create(
                    tipo=autor_data['Tipo'],
                    nome=autor_data['Nome']
                )
                producao.autores.add(autor)

if __name__ == '__main__':
    import_data_from_json()
