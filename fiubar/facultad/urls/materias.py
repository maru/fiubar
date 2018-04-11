# -*- coding: utf-8 -*-
from django.urls import include, path
from django.views.generic.base import RedirectView

from ..views import materias


urlpatterns = [
    path('',
        materias.home,
        name='materias-home'),

    path('<str:cod_materia>/',
        materias.show,
        name='materia-show'),

    #path('search/',
    #    materias.search,
    #    name='materia-search'),
]
