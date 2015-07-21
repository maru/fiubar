# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.sites.models import Site
from website.models import MenuEntry

def site_name(request):
    current_site = Site.objects.get_current()
    return {
        'site_name' : current_site.name,
        'site_url': 'http://%s/' % current_site.domain,
        'site_description': settings.SITE_DESCRIPTION,
        'meta_description': settings.META_DESCRIPTION,
        'meta_keywords': settings.META_KEYWORDS,
    }
    # dict_data['last_login'] = UserSession.objects.get_user_last_login(request.user)

def get_menu_entries(request):
    menu_entries = MenuEntry.objects.get_menu_entries(request.user)
    return {
        'menu_entries' : menu_entries
    }
    return context

