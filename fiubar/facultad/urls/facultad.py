# -*- coding: utf-8 -*-
from django.urls import path
from django.views.generic.base import RedirectView

from ..views import facultad


urlpatterns = [
    # Portada de materias
    path('',
         facultad.HomePageView.as_view(),
         name='home'),

    path('materias/',
         RedirectView.as_view(url='/facultad/'),
         name='materias'),

    path('materias/cargar/',
         facultad.CargarMateriasView.as_view(),
         name='cargar-materias'),

    path('materias/<str:plancarrera>/',
         facultad.PlanCarreraView.as_view(),
         name='materias-carrera'),

    path('materia/<str:codigo>/',
         facultad.MateriaView.as_view(),
         name='materia'),
]
