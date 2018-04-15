# -*- coding: utf-8 -*-
from django.urls import path
from django.views.generic.base import RedirectView

from ..views import facultad


urlpatterns = [
    # Portada de materias
    path('', facultad.home,
         name='home'),

    # Materias de las carreras cursadas.
    # path('materias/', 'plancarrera_all',
    #      name='facultad-materias'),

    path('materias/',
         RedirectView.as_view(url='/facultad/'),
         name='materias'),

    path('materias/cargar/', facultad.cargar_materias,
         name='cargar-materias'),

    path('materias/<str:plancarrera>/', facultad.plancarrera,
         name='materias-carrera'),

    path('materia/<str:codigo>/', facultad.materia,
         name='materia'),
]
