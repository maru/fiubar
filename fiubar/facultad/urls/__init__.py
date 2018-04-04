# -*- coding: utf-8 -*-

app_name = 'facultad'

from . import facultad, carreras

urlpatterns = []
urlpatterns += facultad.urlpatterns
urlpatterns += carreras.urlpatterns
