from django.conf.urls import url
from tastypie.utils import trailing_slash
from recetario.authorization import UserObjectsOnlyAuthorization, \
    RecetasObjectsOnlyAuthorization, ComentariosObjectsOnlyAuthorization
from tastypie.resources import ModelResource
from recetario.authenticate import OAuth20Authentication
from tastypie import fields
from principal.models import User, Receta, Comentario


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        # fields = ['username']
        excludes = ['password']
        authorization = UserObjectsOnlyAuthorization()
        authentication = OAuth20Authentication()

    def dehydrate(self, bundle):
        bundle.data['full_name'] = bundle.obj.first_name + ' ' + bundle.obj.last_name
        return bundle


class UserCreationResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        allowed_methods = ['post']
        resource_name = 'create_user'

    def obj_create(self, bundle, **kwargs):
        user = User.objects.create_user(username=bundle.data["username"], email=bundle.data["email"],
                                        password=bundle.data["password"])
        bundle.obj = user
        return self.full_hydrate(bundle)
        # return super(UserCreationResource, self).obj_create(bundle, user=bundle.request.user)


class RecetaResource(ModelResource):
    usuario = fields.ForeignKey(UserResource, 'usuario', full=False, null=True, blank=True)

    class Meta:
        queryset = Receta.objects.all()
        resource_name = 'receta'
        authorization = RecetasObjectsOnlyAuthorization()
        allowed_methods = ['get', 'post']
        authentication = OAuth20Authentication()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/add%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('create_recipe'), name="create_recipe"),
        ]

    def create_recipe(self, request, **kwargs):
        self.is_authenticated(request)
        self.method_check(request, allowed=['post'])
        fmt = request.META.get('CONTENT_TYPE')

        if fmt.startswith('multipart'):
            data = request.POST.copy()
            data.update(request.FILES)
            titulo = data.get('titulo', '')
            ingredientes = data.get('ingredientes', '')
            preparacion = data.get('preparacion', '')
            imagen = data.get('imagen', '')

            if titulo != '':
                receta = Receta.objects.create(titulo=titulo)

                if ingredientes != '':
                    receta.ingredientes = ingredientes
                if preparacion != '':
                    receta.preparacion = preparacion
                if imagen != '':
                    receta.imagen = imagen

                receta.save()

                bundle = self.build_bundle(obj=receta, request=request)

                return self.create_response(request, {
                    'success': True,
                    'message': 'Created',
                    'obj': self.full_dehydrate(bundle)
                })

            else:
                return self.create_response(request, {
                    'success': False,
                    'code': 2,
                    'message': 'Fill title'
                })
        else:
            return self.create_response(request, {
                'success': False,
                'message': 'Invalid format'
            })


class ComentarioResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    receta = fields.ForeignKey(RecetaResource, 'receta')

    class Meta:
        queryset = Comentario.objects.all()
        resource_name = 'comentario'
        authorization = ComentariosObjectsOnlyAuthorization()
        authentication = OAuth20Authentication()

