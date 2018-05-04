# -*- coding: utf-8 -*-

from . import facultad, carreras

app_name = 'facultad'

urlpatterns = []
urlpatterns += facultad.urlpatterns
urlpatterns += carreras.urlpatterns
