# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView

from . import views


"""fiubar URL Configuration"""
urlpatterns = [
    path('new',
         TemplateView.as_view(template_name='pages/new.html'),
         name='new'),

    path('',
         views.home,
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
]

if getattr(settings, 'DEBUG', False):

    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.conf.urls.static import static

    # This allows the error pages to be debugged during development, just visit
    # these urls in the browser to see how these error pages look like.
    urlpatterns += [
        path('400/',
             default_views.bad_request,
             kwargs={'exception': Exception('Bad Request!')}),
        path('403/',
             default_views.permission_denied,
             kwargs={'exception': Exception('Permission Denied')}),
        path('404/',
             default_views.page_not_found,
             kwargs={'exception': Exception('Page not Found')}),
        path('500/',
             default_views.server_error),
    ]

    # Static and media files
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

    try:
        import debug_toolbar

        urlpatterns += [
            path('__debug__/', include(debug_toolbar.urls)),
        ]
    except ImportError:
        pass
