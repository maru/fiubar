# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('~redirect/',
        view=views.UserRedirectView.as_view(),
        name='redirect'
    ),

    path('<slug:username>/',
        view=views.UserDetailView.as_view(),
        name='detail'
    ),

    path('~update/',
        view=views.ProfileUpdateView.as_view(),
        name='update'
    ),

    path('~account/',
        view=views.UserAccountView.as_view(),
        name='account'
    ),
]
