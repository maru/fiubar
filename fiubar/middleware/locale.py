"This is the locale selecting middleware that will look at accept headers"

from django.conf import settings
from django.core.urlresolvers import (
    LocaleRegexURLResolver, get_resolver, get_script_prefix, is_valid_path,
)
from django.http import HttpResponseRedirect
from django.utils import translation
from django.utils.translation.trans_real import parse_accept_lang_header
from django.utils.cache import patch_vary_headers
from django.utils.functional import cached_property


class DefaultLocaleMiddleware(object):
    """
    This is a very simple middleware that parses a request
    and decides what translation object to install in the current
    thread context. This allows pages to be dynamically
    translated to LANGUAGE_DEFAULT if the user has this language
    in the "Accept-Language" header. Otherwise, the chosen language will be
    any of the available languages.
    """
    response_redirect_class = HttpResponseRedirect

    def process_request(self, request):
        accept = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
        # Keep only the main languages
        accept_languages = [ lang.split('-')[0] for lang, _ in parse_accept_lang_header(accept) ]
        # Sublanguages have minor changes ;)
        if settings.LANGUAGE_DEFAULT.split('_')[0] in accept_languages:
            language = settings.LANGUAGE_DEFAULT
        else:
            language = translation.get_language_from_request(
                request, check_path=self.is_language_prefix_patterns_used)
        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()

    def process_response(self, request, response):
        language = translation.get_language()

        if 'Content-Language' not in response:
            response['Content-Language'] = language
        return response
