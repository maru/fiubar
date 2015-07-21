# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings
from openmate.core import global_urls

urlpatterns = patterns('', 
    # Your urls here
    # (r'^example/', include('example.urls')),
)
urlpatterns += global_urls.urlpatterns

