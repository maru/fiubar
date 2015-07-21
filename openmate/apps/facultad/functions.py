# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
import math

def calculate_time(begin_date, end_date):
    # Calculates total time
    total_time = end_date - begin_date 
    if total_time.days <= 0: 
        return _('???')
    years = total_time.days / 365
    months = (total_time.days % 365) / 30.5
    # Plural
    plural = 's'
    if years == 1: 
        plural = ''
    # -
    if months <= 3:
        return (u'%d año%s') % (years, plural)
    if months <= 7:
        return (u'%d 1/2 año%s') % (years, plural)
    else:
        return (u'%d año%s') % ((years + 1), plural)
