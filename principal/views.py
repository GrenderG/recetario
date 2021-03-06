from django.shortcuts import render_to_response, get_object_or_404
from django.http.response import HttpResponse, HttpResponseRedirect
from django.core.mail import EmailMessage
from django.template.context import RequestContext
from principal.models import Receta, Comentario
from principal.forms import ContactoForm, RecetaForm, ComentarioForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required


def inicio(request):
    recetas = Receta.objects.all()
    return render_to_response('inicio.html', {'recetas': recetas}, context_instance=RequestContext(request))


def usuarios(request):
    users = User.objects.all()
    recetas = Receta.objects.all()
    return render_to_response('usuarios.html', {'usuarios': users, 'recetas': recetas},
                              context_instance=RequestContext(request))


def lista_recetas(request):
    recetas = Receta.objects.all()
    return render_to_response('recetas.html', {'datos': recetas}, context_instance=RequestContext(request))


def detalle_receta(request, id_receta):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ingresar')
    dato = get_object_or_404(Receta, pk=id_receta)
    comentarios = Comentario.objects.filter(receta=dato)
    if request.method == 'POST':
        formulario = ComentarioForm(request.POST, request.FILES)
        f_comentario = formulario.save(commit=False)
        f_comentario.user = request.user
        f_comentario.receta = Receta.objects.get(id=id_receta)
        if formulario.is_valid():
            f_comentario.save()
            return HttpResponseRedirect('/recetario/'+id_receta+'#comentarios')
    else:
        formulario = ComentarioForm
    return render_to_response('receta.html', {'receta': dato, 'comentarios': comentarios, 'formulario': formulario},
                              context_instance=RequestContext(request))

def contacto(request):
    if request.method == 'POST':
        formulario = ContactoForm(request.POST)
        if formulario.is_valid():
            titulo = 'Mensaje desde el recetario'
            contenido = formulario.cleaned_data['mensaje'] + "\n"
            contenido += 'Comunicarse a: ' + formulario.cleaned_data['correo']
            correo = EmailMessage(titulo, contenido, to=['grenderg@gmail.com'])
            correo.send()
            return HttpResponseRedirect('/')
    else:
        formulario = ContactoForm
    return render_to_response('contacto.html', {'formulario': formulario}, context_instance=RequestContext(request))


def nueva_receta(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ingresar')
    if request.method == 'POST':
        formulario = RecetaForm(request.POST, request.FILES)
        f_receta = formulario.save(commit=False)
        f_receta.usuario = request.user
        if formulario.is_valid():
            f_receta.save()
        return HttpResponseRedirect('/recetario')
    else:
        formulario = RecetaForm
    return render_to_response('recetaform.html', {'formulario': formulario}, context_instance=RequestContext(request))


def nuevo_comentario(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ingresar')
    if request.method == 'POST':
        formulario = ComentarioForm(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/recetario')
    else:
        formulario = ComentarioForm
    return render_to_response('comentarioform.html', {'formulario': formulario},
                              context_instance=RequestContext(request))


def nuevo_usuario(request):
    if request.method == 'POST':
        formulario = UserCreationForm(request.POST)
        if formulario.is_valid:
            formulario.save()
            return HttpResponseRedirect('/')
    else:
        formulario = UserCreationForm()
    return render_to_response('nuevousuario.html', {'formulario': formulario},
                              context_instance=RequestContext(request))


def ingresar(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/privado')
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)
                    return HttpResponseRedirect('/privado')
                else:
                    return render_to_response('noactivo.html', context_instance=RequestContext(request))
            else:
                return render_to_response('nousuario.html', context_instance=RequestContext(request))
    else:
        formulario = AuthenticationForm()
    return render_to_response('ingresar.html', {'formulario': formulario},
                              context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def privado(request):
    usuario = request.user
    return render_to_response('privado.html', {'usuario': usuario}, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def cerrar(request):
    logout(request)
    return HttpResponseRedirect('/')