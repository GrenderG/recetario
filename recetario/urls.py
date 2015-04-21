from django.conf.urls import patterns, include, url
from django.contrib import admin
from tastypie.api import Api
from django.conf import settings
from recetario.api import UserResource, RecetaResource, ComentarioResource

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(RecetaResource())
v1_api.register(ComentarioResource())

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^oauth2/', include('provider.oauth2.urls', namespace='oauth2')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sobre/$', 'principal.views.sobre'),
    url(r'^$', 'principal.views.inicio'),
    url(r'^usuarios/$', 'principal.views.usuarios'),
    url(r'^recetario/$', 'principal.views.lista_recetas'),
    url(r'^contacto/$', 'principal.views.contacto'),
    url(r'^recetario/nueva/$', 'principal.views.nueva_receta'),
    url(r'comenta/$', 'principal.views.nuevo_comentario'),
    url(r'usuarios/nuevo$', 'principal.views.nuevo_usuario'),
    url(r'ingresar$', 'principal.views.ingresar'),
    url(r'privado', 'principal.views.privado'),
    url(r'cerrar', 'principal.views.cerrar'),
    (r'api/', include(v1_api.urls)),
    url(r'^recetario/(?P<id_receta>\d+)$', 'principal.views.detalle_receta'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, }
        ),
)
