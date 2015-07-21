# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings
from openmate.core import global_urls
from django.views.generic.simple import direct_to_template, redirect_to

urlpatterns = patterns('',
	# temporary...
	url(r'^home/', redirect_to, {'url' : '/noticias/'}),
	url(r'^$', redirect_to, {'url' : '/noticias/'}),
)

if getattr(settings, 'DEBUG', True):

	urlpatterns += patterns('',

		url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
		  { 'document_root': settings.STATIC_ROOT, 'show_indexes': True, },
		),
		url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
		  { 'document_root': settings.MEDIA_ROOT, 'show_indexes': True, },
		),

	)

urlpatterns += global_urls.urlpatterns
