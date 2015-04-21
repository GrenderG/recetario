# encoding:utf-8
from django.db import models
from django.contrib.auth.models import User


class Receta(models.Model):
    titulo = models.CharField(max_length=100, unique=True)
    ingredientes = models.TextField(help_text='Redacta los ingredientes')
    preparacion = models.TextField(verbose_name='Preparación')
    imagen = models.ImageField(upload_to='recetario', verbose_name='Imágen')
    tiempo_registro = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(User)

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    user = models.ForeignKey(User)
    receta = models.ForeignKey(Receta)
    texto = models.TextField(help_text='Tu comentario', verbose_name='Comentario')

    def __str__(self):
        return self.texto