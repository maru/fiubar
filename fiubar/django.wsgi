import os
import sys
sys.path.append('/usr/local/lib/python2.6/dist-packages/Django-1.2.7')

os.environ['DJANGO_SETTINGS_MODULE'] = 'fiubar.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

path = '/var/lib/fiubar'
if path not in sys.path:
	sys.path.append(path)
