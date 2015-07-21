# -*- coding: utf-8 -*-
"""
URLConf for Django user profile.

"""

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('profiles.views',

    # Show profile.
    url(r'^$', 'show', 
        name='profile-show'),

    # Edit profile info.
    url(r'^edit/$', 'edit', 
        name='profile-edit'),
)

"""
    # Upload photo
    url(r'^edit/photo/$', 'photo_edit', 
        name='profile-photo_edit'),

    # Delete photo
    url(r'^edit/photo/delete/(?P<id>\d+)/$', 'photo_delete', 
        name='profile-photo_delete'),

    # Show photo in profile
    url(r'^edit/photo/set/(?P<id>\d+)/$', 'photo_set_main', 
        name='profile-photo_set_main'),

    # Links to other (internet) profiles.
    url(r'^edit/links/$', 'links', 
        name='profile-links'),
    
    url(r'^edit/links/delete/(?P<type>\w+)/(?P<id>\d+)/$', 'links_delete', 
        name='profile-links_delete'),

    # Email notifications.
    url(r'^notifications/$', 'notifications', 
        name='profile-notifications'),

    # Define visibility.
    #url(r'^privacy/$', 'privacy, 
    #    name='profile-privacy'),


urlpatterns += patterns('django.contrib.auth.views',
    ### Change password
    url(r'^password/change/$', 'password_change', 
        {'template_name': 'password_change_form.html'},
        name='profile-password_change'),

    url(r'^password/change/done/$', 'password_change_done',
        {'template_name': 'password_change_done.html'},
        name='profile-password_change_done'),

)
"""