# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('facultad.views_carreras',

	url(r'^carreras/$', 'home',
		name='carreras-home'),

	url(r'^carreras/add/$', 'add',
		name='carreras-add'),

	url(r'^carreras/delete/$', 'delete',
		name='carreras-show_delete'),

	url(r'^carreras/(?P<plancarrera>\w+)/delete/$', 'delete',
		name='carreras-delete'),

	url(r'^carreras/(?P<plancarrera>\w+)/graduado/$', 'graduado',
		name='carreras-graduado'),

	url(r'^carreras/(?P<plancarrera>\w+)/graduado/del/$', 'del_graduado',
		name='carrera-graduado-del'),

#	url(r'^carreras/(?P<plancarrera>\w+)/alumnos/$', 'alumnos',
#		name='carrera-alumnos'),
)

