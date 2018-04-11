import logging as _logging

from django.conf import settings


LOG_FORMAT = getattr(settings, 'LOG_FORMAT', '[%(asctime)s] %(levelname)-8s %(message)s')
LOG_DATEFMT = getattr(settings, 'LOG_DATEFMT', '%Y-%m-%d %H:%M:%S')
LOG_FILE = getattr(settings, 'LOG_FILE', 'local/fiubar.log')

if getattr(settings, 'DEBUG', False):
	LOG_LEVEL = getattr(settings, 'LOG_LEVEL', _logging.DEBUG)
else:
	LOG_LEVEL = getattr(settings, 'LOG_LEVEL', _logging.INFO)

_logging.basicConfig(
    format   = LOG_FORMAT,
    datefmt  = LOG_DATEFMT,
    level    = LOG_LEVEL
)

logger = _logging.getLogger('fiubar')
fileHandler = _logging.FileHandler(filename = LOG_FILE)
formatter = _logging.Formatter(LOG_FORMAT, LOG_DATEFMT)
fileHandler.setFormatter(formatter)
fileHandler.setLevel(LOG_LEVEL)
logger.addHandler(fileHandler)

def debug(*msgs):
    logger = getlogger()
    logger.debug(', '.join(map(str, msgs)))

"""
class LoggingMiddleware(object):

    def __init__(self):
        self.logger = _logging.getLogger('fiubar')

    def process_request(self, request):
        request.log = []

    def process_view(self, request, view_func, view_args, view_kwargs):
        logger.warning(view_func.__name__ + str(view_args) + str(view_kwargs))

    def process_response(self, request, response):
        for log in request.log:
            self.logger.info(log)
        return response

    def process_exception(self, request, exception):
        self.logger.warn(exception)
"""
