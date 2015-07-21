# -*- coding: utf-8 -*-
"""
Copyright (c) 2007, James Bennett
Copyright (c) 2008, OpenMate - Some changes introduced

URLConf for Django user registration.

"""

from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
	# Activation keys get matched by \w+ instead of the more specific
	# [a-fA-F0-9]+ because a bad activation key should still get to the view;
	# that way it can return a sensible "invalid key" message instead of a
	# confusing 404.

	### Login
	url(r'^login/$',
		'account.views.login',
		{'template_name': 'account/login.html'},
		name='account-login'),

	### Logout
	url(r'^logout/$',
		auth_views.logout,
		{'template_name': 'account/logout.html'},
		name='account-logout'),

	### Reset password
	url(r'^password/reset/$',
		'account.views.password_reset',
		{ 'template_name': 'account/password_reset_form.html',
		  'email_template_name': 'account/password_reset_email.html', },
		name='account-password_reset'),

	url(r'^password/reset/done/$',
		auth_views.password_reset_done,
		{'template_name': 'account/password_reset_done.html'},
		name='account-password_reset_done'),

	### Change password
    url(r'^password/change/$', 'django.contrib.auth.views.password_change',
        {'template_name': 'account/password_change_form.html'},
        name='account-password_change_form'),

    url(r'^password/change/done/$', 'django.contrib.auth.views.password_change_done',
        {'template_name': 'account/password_change_done.html'},
        name='account-password_change_done'),

	url(r'^password/change/(?P<pwdreset_key>\w+)/$',
		'account.views.password_change',
		name='account-password_change'),

	url(r'^$', 'account.views.home',
		name='account-home'),

)
