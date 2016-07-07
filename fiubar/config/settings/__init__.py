# -*- coding: utf-8 -*-

import json
# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.
from django.core.exceptions import ImproperlyConfigured

# JSON-based secrets module
try:
    with open("secrets.json") as f:
        secrets = json.loads(f.read())
except:
    secrets = {}

def get_secret(setting, default=None, secrets=secrets):
    """Get the secret variable or return explicit exception."""
    try:
        return secrets[setting]
    except KeyError:
        if default:
            return default
        error_msg = "Set the {0} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)
