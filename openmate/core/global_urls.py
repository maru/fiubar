# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^account/', include('account.urls')),
	url(r'^account/', include('registration.urls')),
	url(r'^about/', include('about.urls')),
	url(r'^noticias/', include('articles.urls')),
	url(r'^facultad/', include('facultad.urls_facultad')),
	url(r'^profile/', include('profiles.urls')),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^', include('website.urls')),

)
"""
	url(r'^materias/', include('facultad.urls_materias')),
	url(r'^messages/', include('messages.urls')),
	url(r'^user', include('profiles.urls_users')),
	url(r'^groups/', include('groups.urls_groups')),
	url(r'^group/', include('groups.urls_group')),
	url(r'^videos/', include('videos.urls')),
	url(r'^comments/', include('django.contrib.comments.urls')),
	# (r'^search/$', direct_to_template, {'template': 'base_site.html'}, name='search-run'),
"""

# Custom 404 and 500 views
from django.conf.urls.defaults import handler404, handler500
handler404 = 'website.views.page_not_found'
handler500 = 'website.views.server_error'

