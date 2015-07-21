#!/usr/bin/env python
import os
from os.path import abspath, dirname, join
import sys

BASE_DIR = dirname(dirname(abspath(__file__)))
sys.path = [ BASE_DIR, BASE_DIR + '/Django-1.2.7'] + sys.path

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fiubar.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
