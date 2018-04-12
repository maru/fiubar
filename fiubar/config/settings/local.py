# -*- coding: utf-8 -*-
"""
Local settings

- Run in Debug mode
- Use console backend for emails
- Add Django Debug Toolbar
- Add django-extensions as app
"""

import socket

from django.contrib.messages import constants as message_constants

from .common import * # noqa


# DEBUG
# ------------------------------------------------------------------------------
DEBUG = get_secret('DJANGO_DEBUG', default=True)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/2.0/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = get_secret('DJANGO_SECRET_KEY',
                        default='Z&r}+t&ZTLV`*M3`i|50FWCPWfdyuPigh8')

# DATABASE CONFIGURATION
DATABASES['default'] = get_secret('DATABASE_DEFAULT', DATABASES['default'])

MESSAGE_LEVEL = message_constants.DEBUG

# Mail settings
# ------------------------------------------------------------------------------

EMAIL_PORT = 1025

EMAIL_HOST = 'localhost'
EMAIL_BACKEND = get_secret('DJANGO_EMAIL_BACKEND',
                           'django.core.mail.backends.console.EmailBackend')


# CACHING
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

# django-debug-toolbar
# ------------------------------------------------------------------------------
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]

INSTALLED_APPS += ['debug_toolbar', ]

INTERNAL_IPS = ['127.0.0.1', ]
# tricks to have debug toolbar when developing with docker
if get_secret('USE_DOCKER', default='no') == 'yes':
    ip = socket.gethostbyname(socket.gethostname())
    INTERNAL_IPS += [ip[:-1] + "1"]

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

ACCOUNT_DEFAULT_HTTP_PROTOCOL = get_secret('ACCOUNT_DEFAULT_HTTP_PROTOCOL',
                                           default='http')

# ACCOUNT_ADAPTER = 'fiubar.models.SignupClosedAdapter'

ALLOWED_HOSTS = get_secret('DJANGO_ALLOWED_HOSTS',
                           default=['127.0.0.1', 'localhost'])
