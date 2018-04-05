# -*- coding: utf-8 -*-
from django.urls import path
from django.views.generic.base import RedirectView

from ..views import facultad

urlpatterns = [
	# Portada de materias
	path('', facultad.home,
		name='home'),

	# Materias de las carreras cursadas.
	#path('materias/', 'plancarrera_all',
	#	name='facultad-materias'),
	path('materias/',
        RedirectView.as_view(url='/facultad/'),
        name='facultad-materias'),

	path('materias/cargar/', facultad.cargar_materias,
		name='facultad-cargar_materias'),

	path('materias/<str:plancarrera>/', facultad.plancarrera,
		name='facultad-materias-carrera'),

	path('materia/<str:codigo>/', facultad.materia,
		name='facultad-materia'),
]
