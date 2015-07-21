# -*- coding: utf-8 -*-
# Django settings for OpenMate project.
import sys
from os.path import abspath, dirname, join
from django.utils.translation import ugettext_lazy as _

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
	('Webmaster', 'webmaster@localhost'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = ''		   # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = ''			 # Or path to database file if using sqlite3.
DATABASE_USER = ''			 # Not used with sqlite3.
DATABASE_PASSWORD = ''		 # Not used with sqlite3.
DATABASE_HOST = ''			 # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''			 # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be avilable on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Argentina/Buenos_Aires'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es'

LANGUAGES = (
  ('es', _('Spanish')),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds static files.
STATIC_ROOT = '/var/www/openmate/static/'

# URL that handles the static files served from STATIC_ROOT
STATIC_URL = '/static/'

# Absolute path to the directory that holds media.
MEDIA_ROOT = '/var/lib/openmate/media/openmate/'

# URL that handles the media served from MEDIA_ROOT.
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/media/admin/'

BASE_DIR = dirname(__file__)

# Make this unique, and don't share it with anybody.
# SECRET_KEY = open(abspath(join(BASE_DIR, '.openmate-secret'))).read().strip()

# Apps in system path
sys.path.insert(0, abspath(join(BASE_DIR, '../apps')))

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.load_template_source',
	'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
	'django.core.context_processors.auth',
	'django.core.context_processors.debug',
	'django.core.context_processors.i18n',
	'django.core.context_processors.media',
	'django.core.context_processors.request',
	'website.context_processors.site_name',
	'website.context_processors.get_menu_entries',
)

MIDDLEWARE_CLASSES = (
	#'djangologging.middleware.LoggingMiddleware',
	#'django.middleware.cache.UpdateCacheMiddleware',
	#'django.middleware.cache.FetchFromCacheMiddleware',
	'django.middleware.locale.LocaleMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.middleware.csrf.CsrfResponseMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'openmate.urls'

TEMPLATE_DIRS = (
	abspath(join(BASE_DIR, '../templates/')),
)

INSTALLED_APPS = (
	# Django applications
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.admin',
	'django.contrib.humanize',
	'django.contrib.markup',
	'django.contrib.comments',
	'django.contrib.flatpages',

	'website',
	'about',
	'contact_form',
	'account',
	'registration',
	'articles',
	'tagging',
	'facultad',
	'profiles',
)
"""
	# OpenMate modules
	#'polls',
	#'files',
	'groups',
	'messages',
	'videos',
	#'event',
	# 'rating', # Actualizar
	# 'app_plugins', # Actualizar
	# 'rosetta', -> instalar
)"""

DEFAULT_FILE_STORAGE = 'openmate.core.storage.StaticDirSystemStorage'

# Session configuration
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Date and time formats
DATETIME_FORMAT = 'N j, Y, H:i'
DATE_FORMAT = 'd/m/Y'
TIME_FORMAT = 'H:i'

LOGIN_REDIRECT_URL = '/home/'
LOGIN_URL = '/account/login/'
LOGOUT_URL = '/account/logout/'

AUTH_PROFILE_MODULE = 'profiles.Profile'
