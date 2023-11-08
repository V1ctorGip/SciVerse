# producao_cientifica/models.py

from django.db import models

class Autor(models.Model):
    TIPO_CHOICES = [
        ('Principal', 'Principal'),
        # Adicione outros tipos conforme necessário
    ]
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    nome = models.CharField(max_length=255)

class ProducaoCientifica(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    titulo = models.CharField(max_length=255)
    nome_do_curso = models.CharField(max_length=255)
    nome_orientador = models.CharField(max_length=255)
    link_arquivo = models.URLField()
    autores = models.ManyToManyField(Autor)

class Person(models.Model):
    name = models.CharField(max_length=100)
