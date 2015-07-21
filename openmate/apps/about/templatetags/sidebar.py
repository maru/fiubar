# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django import template

register = template.Library()

@register.simple_tag
def sidebar_bugs_title():
    return _(u'Report a bug')

@register.filter
def sidebar_bugs_content(context):
    return {}
register.inclusion_tag('sidebar_bugs.html', takes_context=True)(sidebar_bugs_content)
