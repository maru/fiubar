# -*- coding: utf-8 -*-

from . import facultad, carreras, materias

app_name = 'facultad'

urlpatterns = []
urlpatterns += facultad.urlpatterns
urlpatterns += carreras.urlpatterns
