# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from ..models import Materia

from fiubar.alumnos.models import Materia as AlumnoMateria


context = {}


@login_required
def home(request):
    return render_to_response('materias_home.html', context,
                              context_instance=RequestContext(request))


@login_required
def show(request, cod_materia):
    return render_to_response('materia_show.html', context,
                              context_instance=RequestContext(request))


@login_required
def cursos(request, cod_materia):
    materia = _get_common_vars(cod_materia)
    context['cursando_list'] = AlumnoMateria.objects.filter(materia=materia,
                                                            state='C')
    context['aprobando_list'] = AlumnoMateria.objects.filter(materia=materia).\
        exclude(state='C')
    return render_to_response('materia_cursos.html', context,
                              context_instance=RequestContext(request))


def _get_common_vars(cod_materia):
    context['materia'] = get_object_or_404(Materia, id=cod_materia)
    return context['materia']
