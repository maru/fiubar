# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from profiles.models import Profile, Photo
#from utils import templates as utils

register = template.Library()
@register.simple_tag
def profile_show_avatar(profile, size='s'):
    if type(profile) != Profile:
        profile = Profile.objects.get(user=profile)
    if type(profile) == Profile and profile.photo:
        photo = profile.photo
        path = photo.get_html_path(size)
    else:
        path = '/media/images/img2/avatar_%s.jpg' % size
    return path

def last_new_profiles(context, last=4):
    """Plugin"""
    last_login = context.get('last_login', None)
    profile_list = Profile.objects.get_last(last=last, last_login=last_login)
    #if profile_list: 
    utils.close_plugin(context)
    return { 'profile_list' : profile_list, }
register.inclusion_tag('plugins/last_new_profiles.html', takes_context=True)(last_new_profiles)

def profile_user_menu(context):
    """Plugin"""
    profile = Profile.objects.get(user=context['user'])
    return { 'profile' : profile }
register.inclusion_tag('plugins/profile_user_menu.html', takes_context=True)(profile_user_menu)

print 2
