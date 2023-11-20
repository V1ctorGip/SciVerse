from django.shortcuts import render
from django.db.models import Q, Value
from django.db.models import Count
from collections import Counter
import json
from collections import defaultdict
from django.db.models.functions import Concat
from .models import ProducaoCientifica, Autor 
from .models import Person
from producao_cientifica.tables import PersonTable
from producao_cientifica.models import ProducaoCientifica
from django.http import JsonResponse

def home(request):
    total_publicacoes = ProducaoCientifica.objects.count()
    context = {
        'total_publicacoes': total_publicacoes
    }
    return render(request, 'home.html', context)

def home(request):
    total_publicacoes = ProducaoCientifica.objects.count()
    
    # Conta o número de orientadores distintos
    distinct_orientadores_count = ProducaoCientifica.objects.values('nome_orientador').distinct().count()

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

def lista_orientadores(request):
    search_query = request.GET.get('search', '')
    if search_query:
        orientadores = ProducaoCientifica.objects.values_list('nome_orientador', flat=True).distinct().filter(nome_orientador__icontains=search_query).order_by('nome_orientador')
    else:
        orientadores = ProducaoCientifica.objects.values_list('nome_orientador', flat=True).distinct().order_by('nome_orientador')
    return render(request, 'lista_orientadores.html', {'orientadores': orientadores})

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
        # Converta a query para int se for possível, caso contrário, use 0
        query_as_int = int(query) if query.isdigit() else 0
        publicacoes = ProducaoCientifica.objects.filter(
            Q(titulo__icontains=query) | 
            Q(nome_do_curso__icontains=query) |
            Q(nome_orientador__icontains=query) |
            Q(autores__nome__icontains=query) |
            Q(id=query_as_int)  # Adicione esta linha para permitir pesquisa por ID
        ).distinct().order_by('titulo')

    # Use annotate para adicionar o nome do autor principal ao queryset
    publicacoes = publicacoes.annotate(
        nome_autor_principal=Concat(
            'autores__nome',
            Value(' '),
            filter=Q(autores__tipo='Principal')
        )
    )

    # Ajuste os nomes dos campos para corresponder ao seu modelo
    publicacoes_list = list(publicacoes.values(
        'id', 'titulo', 'nome_do_curso', 'nome_orientador', 'nome_autor_principal', 'link_arquivo'
    ))

    return JsonResponse(publicacoes_list, safe=False)

#####################################################################

def get_nome_autor_principal(publicacao):
    autores_qs = publicacao.autores.all()
    return autores_qs[0].nome if autores_qs.exists() else 'Autor desconhecido'

def lista_de_publicacoes(request):
    publicacoes_qs = ProducaoCientifica.objects.all()
    publicacoes = []

    for publicacao in publicacoes_qs:
        nome_autor_principal = get_nome_autor_principal(publicacao)  
        
        publicacoes.append({
            'Id': publicacao.id,  
            'Titulo': publicacao.titulo,  
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
    # Contar as produções por curso
    contador_cursos = ProducaoCientifica.objects.values('nome_do_curso').annotate(total=Count('id')).order_by('nome_do_curso')

    # Converter o QuerySet em um dicionário para o JsonResponse
    dados = {item['nome_do_curso']: item['total'] for item in contador_cursos}

    return JsonResponse(dados)