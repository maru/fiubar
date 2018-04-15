# -*- coding: utf-8 -*-
from django.urls import path
from django.views.generic import TemplateView

from . import views


app_name = 'users'
urlpatterns = [
    path('',
         TemplateView.as_view(template_name='users/user_profile.html'),
         name='profile'),

    path('~redirect/',
         view=views.UserRedirectView.as_view(),
         name='redirect'),

    path('~update/',
         view=views.ProfileUpdateView.as_view(),
         name='update'),

    path('~account/',
         view=views.UserAccountView.as_view(),
         name='account'),

    path('<slug:username>/',
         view=views.UserDetailView.as_view(),
         name='detail'),
]
