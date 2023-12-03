# producao_cientifica/models.py
from datetime import date
from django.db import models

class Autor(models.Model):
    TIPO_CHOICES = [
        ('Principal', 'Principal'),
        # Adicione outros tipos conforme necessário
    ]
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    nome = models.CharField(max_length=255)

class PalavraChave(models.Model):
    termo = models.CharField(max_length=100)

class ProducaoCientifica(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    titulo = models.CharField(max_length=255)
    data_da_defesa = models.DateField(default=date.today)
    nome_do_curso = models.CharField(max_length=255)
    nome_orientador = models.CharField(max_length=255)
    link_arquivo = models.URLField()
    autores = models.ManyToManyField(Autor)
    palavras_chave = models.ManyToManyField(PalavraChave)
    PalavrasChave = models.TextField()

class Person(models.Model):
    name = models.CharField(max_length=100)
