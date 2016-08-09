# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^~redirect/$',
        view=views.UserRedirectView.as_view(),
        name='redirect'
    ),

    url(
        regex=r'^(?P<username>[\w]+)/$',
        view=views.UserDetailView.as_view(),
        name='detail'
    ),

    url(
        regex=r'^~update/$',
        view=views.ProfileUpdateView.as_view(),
        name='update'
    ),

    url(
        regex=r'^~account/$',
        view=views.UserAccountView.as_view(),
        name='account'
    ),
]
