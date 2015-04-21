# encoding:utf-8
__author__ = 'Becario'

from django.forms import ModelForm
from django import forms
from principal.models import Receta, Comentario


class ContactoForm(forms.Form):
    correo = forms.EmailField(label='Tu email')
    mensaje = forms.CharField(widget=forms.Textarea)


class RecetaForm(ModelForm):
    class Meta:
        model = Receta


class ComentarioForm(ModelForm):
    class Meta:
        model = Comentario