# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from . import urls_local, views


"""fiubar URL Configuration"""
urlpatterns = [
    path('',
         views.HomePageView.as_view(),
         name='home'),

    path('about/',
         TemplateView.as_view(template_name='pages/about.html'),
         name='about'),

    path('faq/',
         TemplateView.as_view(template_name='pages/faq.html'),
         name='faq'),

    path('tos/',
         TemplateView.as_view(template_name='pages/tos.html'),
         name='tos'),

    path('contact/', include('contact_form.recaptcha_urls')),

    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),

    # User management
    path('users/',
         include('fiubar.users.urls', namespace='users')),

    path('accounts/',
         include('allauth.urls')),

    path('facultad/',
         include('fiubar.facultad.urls', namespace='facultad')),

    path('api/', include('fiubar.api.urls')),
]

urlpatterns += urls_local.urlpatterns
