# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from facultad.models import Alumno

"""
carreras = cache.get(c.CACHE_CARRERAS % str(request.user.id))
if not carreras:
    carreras = Alumno.objects.select_related(depth=1).filter(user=request.user)
    if not carreras:
        # User has to choose a carrera
        request.user.message_set.create(message=_(u'¿Qué carrera cursás?'))
        return None 
    cache.set(c.CACHE_CARRERAS % str(request.user.id), carreras)
"""
def get_carreras(function):
    """
    Decorator for views that checks if user está cursando alguna 
    carrera.
    """
    def f(request, *args, **kwargs):
        carreras = Alumno.objects.select_related(depth=1).filter(user=request.user).order_by('plancarrera')
        if not carreras:
            # User has to choose a carrera
            if not function.__name__ == 'add':
                request.user.message_set.create(message=_(u'¿Qué carrera cursás?'))
                return HttpResponseRedirect(reverse('carreras-add'))
        request.session['list_carreras'] = [c for c in carreras] 
        return function(request, *args, **kwargs)
        
    f.__doc__  = function.__doc__
    f.__name__ = function.__name__
    return f
