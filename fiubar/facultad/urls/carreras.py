# -*- coding: utf-8 -*-
from django.urls import path

from ..views import carreras


urlpatterns = [

    path('carreras/', carreras.home,
         name='carreras-home'),

    path('carreras/add/', carreras.add,
         name='carreras-add'),

    path('carreras/delete/', carreras.delete,
         name='carreras-show_delete'),

    path('carreras/<str:plancarrera>/delete/', carreras.delete,
         name='carreras-delete'),

    path('carreras/<str:plancarrera>/graduado/', carreras.graduado,
         name='carreras-graduado'),

    path('carreras/<str:plancarrera>/graduado/del/', carreras.del_graduado,
         name='carrera-graduado-del'),

]
