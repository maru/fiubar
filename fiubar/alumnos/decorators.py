# -*- coding: utf-8 -*-
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import ugettext as _

from .models import PlanCarrera


def get_carreras(function):
    """
    Decorator for views that checks if user está cursando alguna
    carrera.
    """
    def f(request, *args, **kwargs):
        carreras = PlanCarrera.objects.select_related('carrera').\
            filter(user=request.user).order_by('plancarrera')
        if not carreras:
            # User has to choose a carrera
            if not function.__name__ == 'add':
                messages.add_message(request, messages.INFO,
                                     _('¿Qué carrera cursás?'))
                return HttpResponseRedirect(reverse('facultad:carreras-add'))
        request.session['list_carreras'] = [c for c in carreras]
        return function(request, *args, **kwargs)

    f.__doc__ = function.__doc__
    f.__name__ = function.__name__
    return f
