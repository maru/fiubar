"This is the locale selecting middleware that will set the website language"

from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin


class DefaultLocaleMiddleware(MiddlewareMixin):
    """
    This is a very simple middleware that sets the language of the
    website to the default language configured in the settings file.
    """
    response_redirect_class = HttpResponseRedirect

    def process_request(self, request):
        # Only one language
        language = settings.LANGUAGE_DEFAULT
        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()

    def process_response(self, request, response):
        return response
