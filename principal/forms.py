# encoding:utf-8
__author__ = 'Becario'

from django.forms import ModelForm, TextInput, Textarea
from django import forms
from principal.models import Receta, Comentario


class ContactoForm(forms.Form):
    correo = forms.EmailField(label='Tu email', widget=forms.TextInput(attrs={'class': 'form-control'}))
    mensaje = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'style': 'resize:none;'}))

    class Meta:
        widgets = {
            'correo': TextInput(attrs={'class': 'form-control'}),
            'mensaje': Textarea(attrs={'class': 'form-control', 'style': 'resize:none;'}),
        }


class RecetaForm(ModelForm):
    class Meta:
        model = Receta
        exclude = ["usuario"]
        widgets = {
            'titulo': TextInput(attrs={'class': 'form-control'}),
            'ingredientes': Textarea(attrs={'class': 'form-control', 'style': 'resize:none;'}),
            'preparacion': Textarea(attrs={'class': 'form-control', 'style': 'resize:none;'}),
        }


class ComentarioForm(ModelForm):
    class Meta:
        model = Comentario
        exclude = ["user", "receta"]
        widgets = {
            'texto': Textarea(attrs={'class': 'form-control', 'style': 'resize:none;'}),
        }