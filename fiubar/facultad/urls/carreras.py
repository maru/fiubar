# -*- coding: utf-8 -*-
from django.urls import path

from ..views import carreras


urlpatterns = [

    path('carreras/',
         carreras.HomePageView.as_view(),
         name='carreras-home'),

    path('carreras/add/',
         carreras.AddView.as_view(),
         name='carreras-add'),

    path('carreras/delete/',
         carreras.DeleteView.as_view(),
         name='carreras-show_delete'),

    path('carreras/delete/<str:plancarrera>/',
         carreras.DeleteView.as_view(),
         name='carreras-delete'),

    path('carreras/graduado/<str:plancarrera>/',
         carreras.GraduadoView.as_view(),
         name='carreras-graduado'),

    path('carreras/graduado/delete/<str:plancarrera>/',
         carreras.GraduadoDeleteView.as_view(),
         name='carreras-graduado-delete'),

]
