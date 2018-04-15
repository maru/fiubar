# -*- coding: utf-8 -*-
"""
Django settings for fiubar project.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
import json
import os


BASE_DIR = os.path.abspath('')
FIUBAR_DIR = os.path.join(BASE_DIR, 'fiubar')

# JSON-based secrets module
try:
    secret_file = os.getenv("FIUBAR_SECRET_FILE")
    with open(secret_file) as f:
        secrets = json.loads(f.read())
except (IOError, TypeError):
    secrets = {}


def get_secret(setting, default=None):
    """
    Get the value of a Django setting, return None if it doesn't exist.
    The optional second argument can specify an alternate default.
    """
    try:
        return secrets[setting]
    except KeyError:
        return default


# APP CONFIGURATION
# ------------------------------------------------------------------------------
# Default Django apps:
DJANGO_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.admin',
    'captcha',
]
# Other apps
THIRD_PARTY_APPS = [
    'crispy_forms',  # Form layouts
    'allauth',  # registration
    'allauth.account',  # registration
    'allauth.socialaccount',  # registration
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.openid',
    'allauth.socialaccount.providers.linkedin',
]

# Fiubar apps
LOCAL_APPS = [
    'fiubar.users.apps.UsersConfig',
    'fiubar.facultad.apps.FacultadConfig',
]

# See: https://docs.djangoproject.com/en/2.0/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'fiubar.middleware.locale.DefaultLocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# MIGRATIONS CONFIGURATION
# ------------------------------------------------------------------------------
MIGRATION_MODULES = {
}

# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/2.0/ref/settings/#debug
DEBUG = False

# FIXTURE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/2.0/ref/settings/#std:setting-FIXTURE_DIRS # noqa
FIXTURE_DIRS = (
    os.path.join(FIUBAR_DIR, 'fixtures'),
    os.path.join(BASE_DIR, 'fixtures'),
)

# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_BACKEND = get_secret('DJANGO_EMAIL_BACKEND',
                           'django.core.mail.backends.smtp.EmailBackend')

# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/2.0/ref/settings/#admins
ADMINS = (
    ("""Admin""", 'admin@fiubar.tk'),
)

# See: https://docs.djangoproject.com/en/2.0/ref/settings/#managers
MANAGERS = ADMINS

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.abspath(os.path.join(BASE_DIR, 'local/db.sqlite3'))
    }
}
DATABASES['default']['ATOMIC_REQUESTS'] = True


# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = get_secret('TIME_ZONE', default='America/Argentina/Buenos_Aires')

# See: https://docs.djangoproject.com/en/2.0/ref/settings/#language-code
LANGUAGE_CODE = 'en'
LANGUAGE_DEFAULT = 'es_AR'
LANGUAGES = [('es-AR', 'Argentinian Spanish'),
             ('es_AR', 'Argentinian Spanish'),
             ('es', 'Spanish'), ]
LOCALE_PATHS = [
    os.path.join(FIUBAR_DIR, 'locale'),
]

# See: https://docs.djangoproject.com/en/2.0/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/2.0/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/2.0/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/2.0/ref/settings/#use-tz
USE_TZ = True

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/2.0/ref/settings/#templates
TEMPLATES = [
    {
        # See: https://docs.djangoproject.com/en/2.0/ref/settings/#std:setting-TEMPLATES-BACKEND # noqa
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # See: https://docs.djangoproject.com/en/2.0/ref/settings/#template-dirs # noqa
        'DIRS': [
            os.path.join(FIUBAR_DIR, 'templates'),
        ],
        'OPTIONS': {
            # See: https://docs.djangoproject.com/en/2.0/ref/settings/#template-debug # noqa
            'debug': DEBUG,
            # See: https://docs.djangoproject.com/en/2.0/ref/settings/#template-loaders # noqa
            # https://docs.djangoproject.com/en/2.0/ref/templates/api/#loader-types # noqa
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            # See: https://docs.djangoproject.com/en/2.0/ref/settings/#template-context-processors # noqa
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# See: http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs # noqa
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/2.0/ref/settings/#static-url
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(FIUBAR_DIR, 'static'),
)

# See: https://docs.djangoproject.com/en/2.0/ref/contrib/staticfiles/#staticfiles-finders # noqa
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/2.0/ref/settings/#media-root
MEDIA_ROOT = get_secret('MEDIA_ROOT', os.path.join(BASE_DIR, 'local/media'))

# See: https://docs.djangoproject.com/en/2.0/ref/settings/#media-url
MEDIA_URL = '/media/'

# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'fiubar.urls'

# See: https://docs.djangoproject.com/en/2.0/ref/settings/#wsgi-application
WSGI_APPLICATION = 'fiubar.config.wsgi.application'

# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

ACCOUNT_ALLOW_REGISTRATION = get_secret('DJANGO_ACCOUNT_ALLOW_REGISTRATION',
                                        True)

ACCOUNT_ADAPTER = 'fiubar.users.adapters.AccountAdapter'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_DEFAULT_HTTP_PROTOCOL = get_secret('ACCOUNT_DEFAULT_HTTP_PROTOCOL',
                                           default='https')
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_SIGNUP_FORM_CLASS = 'fiubar.forms.SignupForm'
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = False
ACCOUNT_USERNAME_MIN_LENGTH = 3
ACCOUNT_USERNAME_REQUIRED = True

SOCIALACCOUNT_PROVIDERS = {
    "openid": {
        "SERVERS": [{
            "id": "yahoo",
            "name": "Yahoo",
            "openid_url": "http://me.yahoo.com"}]
    }
}
SOCIALACCOUNT_ADAPTER = 'fiubar.users.adapters.SocialAccountAdapter'
SOCIALACCOUNT_AUTO_SIGNUP = False
SOCIALACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_EMAIL_VERIFICATION = False

# Custom user app defaults
AUTH_USER_MODEL = 'users.User'
LOGIN_REDIRECT_URL = 'users:redirect'
LOGIN_URL = 'account_login'

# SLUGLIFIER
AUTOSLUG_SLUGIFY_FUNCTION = 'slugify.slugify'

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators


AUTH_PASSWORD_VALIDATORS = [
    {"NAME": f"django.contrib.auth.password_validation.{name}"}
    for name in [
        "UserAttributeSimilarityValidator",
        "MinimumLengthValidator",
        "CommonPasswordValidator",
        "NumericPasswordValidator"
    ]]

# Location of root django.contrib.admin URL, use {% url 'admin:index' %}
ADMIN_URL = 'admin/'

# ReCaptcha keys
RECAPTCHA_PUBLIC_KEY = get_secret('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = get_secret('RECAPTCHA_PRIVATE_KEY')
NOCAPTCHA = get_secret('RECAPTCHA_NOCAPTCHA', True)
RECAPTCHA_USE_SSL = get_secret('RECAPTCHA_USE_SSL', True)
RECAPTCHA_LANG = get_secret('RECAPTCHA_LANG', 'es-419')
