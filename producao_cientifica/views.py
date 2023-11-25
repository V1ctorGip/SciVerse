from django.shortcuts import render
from django.db.models import Q, Value
from django.db.models import Count,F, Func
from django.db.models.functions import TruncYear
from collections import Counter
import json
from collections import defaultdict
from django.db.models.functions import Concat
from .models import ProducaoCientifica, Autor 
from .models import Person
from producao_cientifica.tables import PersonTable
from producao_cientifica.models import ProducaoCientifica
from django.http import JsonResponse
from django.db.models.functions import ExtractYear
import unicodedata
import re

def home(request):
    total_publicacoes = ProducaoCientifica.objects.count()
    context = {
        'total_publicacoes': total_publicacoes
    }
    return render(request, 'home.html', context)

def normalize_string(s):
    """Remove acentos, espaços e converte para minúsculas."""
    return ''.join(unicodedata.normalize('NFKD', ch).encode('ASCII', 'ignore').decode('ASCII').lower() for ch in s if not ch.isspace())

def home(request):
    total_publicacoes = ProducaoCientifica.objects.count()
    orientadores = set(normalize_string(orientador['nome_orientador']) for orientador in ProducaoCientifica.objects.values('nome_orientador'))
    distinct_orientadores_count = len(orientadores)

    context = {
        'total_publicacoes': total_publicacoes,
        'distinct_orientadores_count': distinct_orientadores_count
    }
    return render(request, 'home.html', context)

def lista_de_publicacoes(request):
    publicacoes = ProducaoCientifica.objects.all()
    context = {
        'publicacoes': publicacoes
    }
    return render(request, 'producao_cientifica/lista_de_publicacoes.html', context)

def normalize_string(s):
    """Remove acentos, espaços e converte para minúsculas."""
    return ''.join(unicodedata.normalize('NFKD', ch).encode('ASCII', 'ignore').decode('ASCII').lower() for ch in s if not ch.isspace())

def lista_orientadores(request):
    search_query = request.GET.get('search', '').lower()
    search_normalized = normalize_string(search_query)

    orientadores_query = ProducaoCientifica.objects.all()
    orientadores_data = {}

    for producao in orientadores_query:
        orientador = producao.nome_orientador
        curso = producao.nome_do_curso

        normalized_orientador = normalize_string(orientador)

        if normalized_orientador not in orientadores_data:
            orientadores_data[normalized_orientador] = {
                'nome_display': orientador, 
                'cursos': set(), 
                'quantidade_orientacoes': 0
            }

        orientadores_data[normalized_orientador]['cursos'].add(curso)
        orientadores_data[normalized_orientador]['quantidade_orientacoes'] += 1

    orientadores_list = sorted(
        (
            {
                'nome_orientador': data['nome_display'],
                'cursos_orientados': ', '.join(data['cursos']),
                'quantidade_orientacoes': data['quantidade_orientacoes'],
            }
            for nome, data in orientadores_data.items()
        ),
        key=lambda x: normalize_string(x['nome_orientador'])  # Ordenação considerando nomes sem espaços e acentos
    )

    if search_query:
        orientadores_list = [
            orientador for orientador in orientadores_list 
            if search_normalized in normalize_string(orientador['nome_orientador']) or 
               search_normalized in normalize_string(orientador['cursos_orientados'])
        ]

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse(orientadores_list, safe=False)

    return render(request, 'lista_orientadores.html', {'orientadores': orientadores_list})

def people(request):
    queryset = Person.objects.all()
    people_table = PersonTable(queryset)
    return render(request, "lista_orientadores.html", {'people_table': people_table})

def ajax_search(request):
    query = request.GET.get('q', '')
    """
    if len(query) >= 3:
        results = ProducaoCientifica.objects.filter(nome_orientador__icontains=query)
        names = list(results.values_list('nome_orientador', flat=True).distinct().order_by('nome_orientador'))
        return JsonResponse(names, safe=False)
    """
    # Se a query estiver vazia, retorne todos os orientadores
    if query == "":
        orientadores = ProducaoCientifica.objects.distinct().order_by('nome_orientador')
    elif len(query) >= 3:
        results = ProducaoCientifica.objects.filter(nome_orientador__icontains=query)
        orientadores = results.distinct().order_by('nome_orientador')
    
    # Converta o queryset em uma lista de nomes e retorne como JSON
    orientadores_list = list(orientadores.values_list('nome_orientador', flat=True))
    return JsonResponse(orientadores_list, safe=False)

def ajax_search_publicacoes(request):
    query = request.GET.get('q', '')

    if query == "":
        publicacoes = ProducaoCientifica.objects.all().order_by('id')
    else:
        publicacoes = ProducaoCientifica.objects.filter(
            Q(titulo__icontains=query) | 
            Q(nome_do_curso__icontains=query) |
            Q(nome_orientador__icontains=query) |
            Q(autores__nome__icontains=query) |
            Q(data_da_defesa__icontains=query) | 
            Q(id=int(query) if query.isdigit() else 0)
        ).distinct().order_by('titulo')

    publicacoes = publicacoes.annotate(
        nome_autor_principal=Concat(
            'autores__nome',
            Value(' '),
            filter=Q(autores__tipo='Principal')
        )
    )

    publicacoes_list = []
    for publicacao in publicacoes:
        publicacoes_list.append({
            'id': publicacao.id,
            'titulo': publicacao.titulo,
            'data_da_defesa': publicacao.data_da_defesa.strftime('%d/%m/%Y') if publicacao.data_da_defesa else '',
            'nome_do_curso': publicacao.nome_do_curso,
            'nome_orientador': publicacao.nome_orientador,
            'nome_autor_principal': publicacao.nome_autor_principal,
            'link_arquivo': publicacao.link_arquivo
        })

    return JsonResponse(publicacoes_list, safe=False)

#####################################################################

def get_nome_autor_principal(publicacao):
    autores_qs = publicacao.autores.all()
    return autores_qs[0].nome if autores_qs.exists() else 'Autor desconhecido'

def lista_de_publicacoes(request):
    publicacoes_qs = ProducaoCientifica.objects.all().order_by('id')
    publicacoes = []

    for publicacao in publicacoes_qs:
        nome_autor_principal = get_nome_autor_principal(publicacao)
        data_formatada = publicacao.data_da_defesa.strftime('%d/%m/%Y') if publicacao.data_da_defesa else ''

        publicacoes.append({
            'Id': publicacao.id,
            'Titulo': publicacao.titulo,
            'DataDaDefesa': data_formatada,  
            'NomeDoCurso': publicacao.nome_do_curso,
            'NomeOrientador': publicacao.nome_orientador,
            'LinkArquivo': publicacao.link_arquivo,
            'NomeAutorPrincipal': nome_autor_principal
        })

    context = {
        'publicacoes': publicacoes
    }
    return render(request, 'producao_cientifica/lista_de_publicacoes.html', context)

def producao_cientifica_por_curso(request):
    contador_cursos = ProducaoCientifica.objects.values('nome_do_curso').annotate(total=Count('id')).order_by('nome_do_curso')

    # Normalizar e contabilizar os cursos
    cursos_normalizados = {}
    for item in contador_cursos:
        nome_curso = item['nome_do_curso'].strip().title() if item['nome_do_curso'] else "Não Informado"
        cursos_normalizados[nome_curso] = cursos_normalizados.get(nome_curso, 0) + item['total']

    return JsonResponse(cursos_normalizados)


def producao_cientifica_por_ano(request):
    # Contar as produções por ano de cada curso
    contador_anos = ProducaoCientifica.objects.annotate(ano=ExtractYear('data_da_defesa')).values('nome_do_curso', 'ano').annotate(total=Count('id')).order_by('nome_do_curso', 'ano')

    # Estrutura de dados para armazenar a contagem
    dados = {}
    for item in contador_anos:
        curso = item['nome_do_curso']  # Certifique-se de que este é o nome correto do campo no seu modelo
        ano = item['ano']
        if curso not in dados:
            dados[curso] = {}
        dados[curso][ano] = item['total']

    return JsonResponse(dados)


def normalize_string(s):
    """Remove acentos, espaços e converte para minúsculas."""
    return ''.join(unicodedata.normalize('NFKD', ch).encode('ASCII', 'ignore').decode('ASCII').lower() for ch in s if not ch.isspace())

def top_orientadores(request):

    orientacoes = ProducaoCientifica.objects.all()
    orientacoes_count = {}

    for orientacao in orientacoes:
    
        normalized_nome = normalize_string(orientacao.nome_orientador)

        if normalized_nome in orientacoes_count:
            orientacoes_count[normalized_nome]['total'] += 1
        else:
            orientacoes_count[normalized_nome] = {'nome_display': orientacao.nome_orientador, 'total': 1}

  
    dados = sorted(
        ((data['nome_display'], data['total']) for nome, data in orientacoes_count.items()), 
        key=lambda x: x[1], 
        reverse=True
    )[:20]

    dados_formatados = {item[0]: item[1] for item in dados}

    return JsonResponse(dados_formatados)



def palavras_chave_emergentes_por_ano(request):
    producoes = ProducaoCientifica.objects.annotate(
        ano=TruncYear('data_da_defesa')
    ).values('ano', 'palavras_chave__termo')

    frequencia_por_ano = {}
    for producao in producoes:
        ano = producao['ano'].year
        termo = producao['palavras_chave__termo']
        if ano not in frequencia_por_ano:
            frequencia_por_ano[ano] = {}
        if termo:
            frequencia_por_ano[ano][termo] = frequencia_por_ano[ano].get(termo, 0) + 1

    resultado = {}
    for ano, palavras in frequencia_por_ano.items():
        mais_frequente, freq = max(palavras.items(), key=lambda item: item[1], default=('', 0))
        resultado[ano] = {'termo': mais_frequente, 'frequencia': freq}

    return JsonResponse(resultado)