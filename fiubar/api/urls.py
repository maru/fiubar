from django.conf.urls import include, url
from rest_framework import routers

from fiubar.api import views


router = routers.DefaultRouter()
router.register(r'alumnos', views.AlumnoViewSet)
router.register(r'alumnomaterias', views.AlumnoMateriaViewSet)
router.register(r'carreras', views.CarreraViewSet)
router.register(r'correlativas', views.CorrelativaViewSet)
router.register(r'departamentos', views.DepartamentoViewSet)
router.register(r'materias', views.MateriaViewSet)
router.register(r'plancarreras', views.PlanCarreraViewSet)
router.register(r'planmaterias', views.PlanMateriaViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework'))
]
