# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import redirect_to

urlpatterns = patterns('facultad.views_facultad',

	# Portada de materias
	url(r'^$', 'home',
		name='facultad-home'),

	# Materias de las carreras cursadas.
	#url(r'^materias/$', 'plancarrera_all',
	#	name='facultad-materias'),
	url(r'^materias/$',
        redirect_to, {'url': '/facultad/'},
        name='facultad-materias'),

	url(r'^materias/cargar/$', 'cargar_materias',
		name='facultad-cargar_materias'),

	url(r'^materias/(?P<plancarrera>\w+)/$', 'plancarrera',
		name='facultad-materias-carrera'),

	url(r'^materia/(?P<codigo>\w+)/$', 'materia',
		name='facultad-materia'),
)

"""
	url(r'^calendario/$', 'events',
		name='facultad-events'),

	url(r'^calendario/add/$', 'events_add',
		name='facultad-events_add'),
"""

# Add carreras urls.
from facultad import urls_carreras
urlpatterns += urls_carreras.urlpatterns
