from django.urls import include, path
from rest_framework import routers

from fiubar.api import views


router = routers.DefaultRouter()
router.register(r'alumnos/plancarreras', views.AlumnoViewSet)
router.register(r'alumnos/materias', views.AlumnoMateriaViewSet)
router.register(r'facultad/carreras', views.CarreraViewSet)
router.register(r'facultad/correlativas', views.CorrelativaViewSet)
router.register(r'facultad/departamentos', views.DepartamentoViewSet)
router.register(r'facultad/materias', views.MateriaViewSet)
router.register(r'facultad/plancarreras', views.PlanCarreraViewSet)
router.register(r'facultad/planmaterias', views.PlanMateriaViewSet)


urlpatterns = [
    path(r'', include(router.urls)),

    path(r'facultad/carreras/<str:pk>/plancarreras/',
         views.CarreraViewSet.get_plancarreras,
         name='carrera-plancarreras'),

    path(r'facultad/plancarreras/<str:pk>/planmaterias/',
         views.PlanCarreraViewSet.get_planmaterias,
         name='plancarrera-planmaterias'),

    path(r'auth/',
         include('rest_framework.urls', namespace='rest_framework'))
]
