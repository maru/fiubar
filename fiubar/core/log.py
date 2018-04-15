import logging as _logging

from django.conf import settings


LOG_FORMAT = getattr(settings, 'LOG_FORMAT',
                     '[%(asctime)s] %(levelname)-8s %(message)s')
LOG_DATEFMT = getattr(settings, 'LOG_DATEFMT', '%Y-%m-%d %H:%M:%S')
LOG_FILE = getattr(settings, 'LOG_FILE', 'local/fiubar.log')

if getattr(settings, 'DEBUG', False):
    LOG_LEVEL = getattr(settings, 'LOG_LEVEL', _logging.DEBUG)
else:
    LOG_LEVEL = getattr(settings, 'LOG_LEVEL', _logging.INFO)

_logging.basicConfig(format=LOG_FORMAT,
                     datefmt=LOG_DATEFMT,
                     level=LOG_LEVEL)

logger = _logging.getLogger('fiubar')
fileHandler = _logging.FileHandler(filename=LOG_FILE)
formatter = _logging.Formatter(LOG_FORMAT, LOG_DATEFMT)
fileHandler.setFormatter(formatter)
fileHandler.setLevel(LOG_LEVEL)
logger.addHandler(fileHandler)
