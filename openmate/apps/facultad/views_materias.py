# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
# from django.core.cache import cache
from django.http import Http404, HttpResponseRedirect, HttpResponse, HttpResponseServerError

from facultad.models import Materia, MateriaCurso
from django.core.exceptions import ObjecthoesNotExist
from facultad.models import AlumnoMateria
#from event.models import EventMateria, Event
#from groups.models import Group, Member
#from files.models import File
from openmate.core.log import logger
import datetime

dict_data = {}

@login_required
def home(request):
	# Change
	#from files.models import File
	#dict_data['files_list'] = File.objects.filter().order_by('-id')[:10]

	return render_to_response('materias_home.html', dict_data,
							  context_instance=RequestContext(request))
@login_required
def show(request, cod_materia):
	materia = _get_common_vars(cod_materia)
	dict_data['members_list'] = Member.objects.get_members(dict_data['group'])[:10]
	#dict_data['files_list'] = File.objects.filter(folder__group=dict_data['group']).order_by('-id')[:5]
	return render_to_response('materia_show.html', dict_data,
							  context_instance=RequestContext(request))

@login_required
def cursos(request, cod_materia):
	materia = _get_common_vars(cod_materia)
	dict_data['cursando_list'] = AlumnoMateria.objects.filter(materia=materia, state='C')
	dict_data['aprobando_list'] = AlumnoMateria.objects.filter(materia=materia).exclude(state='C')
	return render_to_response('materia_cursos.html', dict_data,
							  context_instance=RequestContext(request))

@login_required
def events(request, cod_materia):
	materia = _get_common_vars(cod_materia)
	dict_data['event_list'] = EventMateria.objects.get_next_events(materia)
	return render_to_response('materia_events.html', dict_data,
							  context_instance=RequestContext(request))

@login_required
def events_add(request, cod_materia):
	materia = _get_common_vars(cod_materia)
	#from event.forms import CreateEventForm
	if request.method == 'POST':
		form = CreateEventForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data['title']
			where = form.cleaned_data['where']
			description = form.cleaned_data['description']
			date_event = form.cleaned_data['date_event']
			event = Event.objects.create(title=title, where=where, description=description, date=date_event)
			EventMateria.objects.create(event=event, user=request.user, materia=materia)
			request.user.message_set.create(message=_('Fecha agregada'))
			logger.info("%s - materias-events_add: id %s, user '%s', materia '%s', '%s', '%s', '%s', '%s'" %
				(request.META.get('REMOTE_ADDR'), event.id, request.user, materia.id, title, where, date_event, description))
		else:
			logger.error("%s - materias-events_add: user '%s', materia '%s', title '%s', where '%s', date_event '%s/%s/%s %s:%s', description '%s'" %
				(request.META.get('REMOTE_ADDR'), request.user, materia.id, form.data['title'], form.data['where'],
				 form.data['date_day'], form.data['date_month'], form.data['date_year'], form.data['time_hour'],
				 form.data['time_minute'], form.data['description']))
	else:
		form = CreateEventForm()
	dict_data['form'] = form
	return render_to_response('materia_events_add.html', dict_data,
							  context_instance=RequestContext(request))

@login_required
def events_delete(request, cod_materia, id_event):
	materia = _get_common_vars(cod_materia)
	event = get_object_or_404(EventMateria, id=id_event, user=request.user)
	logger.info("%s - materias-events_delete: id %s, user '%s'" % (request.META.get('REMOTE_ADDR'), event.id, request.user))
	event.event.delete()
	event.delete()
	request.user.message_set.create(message=_('Fecha borrada'))
	return HttpResponseRedirect(materia.url_events())

@login_required
def get_cursos(request, cod_materia, cuatrimestre):
	materia = _get_common_vars(cod_materia)
	cuat, year = cuatrimestre.split('-')
	dict_cursada_cuat = { 'V' : 2, '1' : 3, '2' : 8 }
	d = datetime.date(int(year), dict_cursada_cuat.get(cuat, 1), 1)
	l = MateriaCurso.objects.filter(materia__id=cod_materia, pub_date=d)
	if request.POST.get('xhr'):
		return HttpResponse(content='')
	return HttpResponse(content=l.values_list)

def _get_common_vars(cod_materia):
	dict_data['materia'] = get_object_or_404(Materia, id=cod_materia)
	try:
		dict_data['group'] = Group.objects.get(email=dict_data['materia'].group_name())
	except:
		dict_data['group'] = None
	return dict_data['materia']

