# -*- coding: utf-8 -*-
import sys, os
from os.path import abspath, dirname, join

from openmate.core.global_settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

BASE_DIR = dirname(dirname(abspath(__file__)))

ADMINS = (
   ('Admin', 'admin@fiubar.com.ar'),
)
MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'     # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME = 'db.sqlite3'			 # Or path to database file if using sqlite3.

ROOT_URLCONF = 'fiubar.urls'
MEDIA_ROOT = BASE_DIR + '/fiubar/media/'
STATIC_ROOT = BASE_DIR + '/fiubar/static/'
STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    BASE_DIR + '/fiubar/templates/',
)

INTERNAL_IPS = ('127.0.0.1')

SITE_DESCRIPTION = 'Fiubar'
META_DESCRIPTION = 'Fiubar'
META_KEYWORDS = 'Fiubar, noticias, articulos, ciencia, ingenieria, tecnologia'

LOG_FILE = BASE_DIR + '/fiubar.log'

DEFAULT_FROM_EMAIL = 'Admin Fiubar <admin@fiubar.com.ar>'

from fiubar.bin import check_padron
CHECK_PADRON = check_padron

