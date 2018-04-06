# -*- coding: utf-8 -*-
import datetime

from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from fiubar.core.log import logger

from ..models.models import Materia, AlumnoMateria

context = {}

@login_required
def home(request):
	return render_to_response('materias_home.html', context,
							  context_instance=RequestContext(request))
@login_required
def show(request, cod_materia):
	materia = _get_common_vars(cod_materia)
	context['members_list'] = Member.objects.get_members(context['group'])[:10]
	return render_to_response('materia_show.html', context,
							  context_instance=RequestContext(request))

@login_required
def cursos(request, cod_materia):
	materia = _get_common_vars(cod_materia)
	context['cursando_list'] = AlumnoMateria.objects.filter(materia=materia, state='C')
	context['aprobando_list'] = AlumnoMateria.objects.filter(materia=materia).exclude(state='C')
	return render_to_response('materia_cursos.html', context,
							  context_instance=RequestContext(request))

def _get_common_vars(cod_materia):
	context['materia'] = get_object_or_404(Materia, id=cod_materia)
	try:
		context['group'] = Group.objects.get(email=context['materia'].group_name())
	except:
		context['group'] = None
	return context['materia']
