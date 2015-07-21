# -*- coding: utf-8 -*-
"""
URLConf for Django member profile.

"""

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('profiles.views',

    # Show all member profiles
    url(r'^s/search/$', 'search',
        name='member-search'),
        
    # Show all member profiles
    url(r'^s/$', 'list_users',
        name='member-show_all'),

    # Show member profile
    url(r'^/(?P<username>\w+)/$', 'show',
        name='member-profile_show'),

)
