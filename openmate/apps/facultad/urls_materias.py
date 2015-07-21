# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url, include
from django.views.generic.simple import redirect_to

urlpatterns = patterns('facultad.views_materias',
    url(r'^$',
        'home',
    #    redirect_to,
    #    {'url': '/facultad/'},
        name='materias-home'),

    url(r'^(?P<cod_materia>\w+)/$',
        'show',
        name='materia-show'),

    #url(r'^search/$',
    #    materias.search,
    #    name='materia-search'),

    #url(r'^(?P<cod_materia>\w+)/info/',
    #    include('polls.urls.encuestas')),

    #url(r'^(?P<cod_materia>\w+)/encuestas/',
    #    include('polls.urls.encuestas')),

    url(r'^(?P<cod_materia>\w+)/files',
        include('files.urls'),
        name='materia-files'),

    #url(r'^(?P<cod_materia>\w+)/links/',
    #    include('polls.urls.encuestas')),

    url(r'^(?P<cod_materia>\w+)/group/',
        redirect_to, {'url': '/group/fiuba-%(cod_materia)s/'},
        name='materia-group'),

    url(r'^(?P<cod_materia>\w+)/alumnos/$',
        'cursos',
        name='materia-cursos'),

    url(r'^(?P<cod_materia>\w+)/calendario/$',
        'events',
        name='materia-events'),

    url(r'^(?P<cod_materia>\w+)/calendario/add/$',
        'events_add',
        name='materia-events_add'),

    url(r'^(?P<cod_materia>\w+)/calendario/delete/(?P<id_event>\w+)/$',
        'events_delete',
        name='materia-events_delete'),

    url(r'^(?P<cod_materia>\w+)/cursos/(?P<cuatrimestre>\w+-\w+)/$',
        'get_cursos',
        name='materia-get_cursos'),

)
