# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from facultad.decorators import get_carreras
from facultad.models import PlanMateria, Alumno, Carrera, AlumnoMateria, AlumnoCurso, Materia, MateriaCurso
from facultad import sist_acad
from facultad.forms import CursadaForm
from openmate.core.log import logger
#from event.forms import CreateEventMateriaForm
#from event.models import EventMateria, Event
import datetime

dict_data = {}

@login_required
@get_carreras
def home(request):
	# Carreras and Materias
	dict_data['list_carreras'] = request.session.get('list_carreras', list())
	dict_data['list_matcur'] = AlumnoMateria.objects.get_summary(request.user)
	return render_to_response('facultad/home.html', dict_data,
							  context_instance=RequestContext(request))

@login_required
@get_carreras
def plancarrera_all(request):
	dict_data['list_carreras'] = request.session.get('list_carreras', list())
	# Menu
	dict_data.update(_menu_materias(request.GET))
	dict_data['th_correlativas'] = _(u' ')
	# Materias
	if dict_data['tab_selected'] == 'cursando':
		# Busco las que están en  AlumnoMateria y no aprobadas
		lista_materias = AlumnoMateria.objects.list_materias_cursando(request.user).order_by('state')
		dict_data['th_estado'] = _(u'Estado')
	elif dict_data['tab_selected'] == 'aprobadas':
		# Busco las que están en  AlumnoMateria y aprobadas
		lista_materias = AlumnoMateria.objects.list_materias_aprobadas(request.user)
		dict_data['th_estado'] = _(u'Aprobada')
		dict_data['th_correlativas'] = u'Nota '
	else:
		raise Http404(_('Error 404'))

	dict_data['lista_materias'] = lista_materias
	return render_to_response('facultad/plancarrera_all.html', dict_data,
							  context_instance=RequestContext(request))

@login_required
@get_carreras
def plancarrera(request, plancarrera):
	dict_data['list_carreras'] = request.session.get('list_carreras', list())

	# Get carrera y plan
	request.session['plancarrera'] = plancarrera
	alumno = get_object_or_404(Alumno, plancarrera__short_name=plancarrera, user=request.user)
	dict_data['carrera'] = alumno.carrera
	plancarrera = alumno.plancarrera
	dict_data['plancarrera'] = plancarrera

	# Menu
	dict_data.update(_menu_materias(request.GET))
	dict_data['th_correlativas'] = _(u' ')
	# Materias
	if dict_data['tab_selected'] == 'cursando':
		# Busco las que están en  AlumnoMateria y no aprobadas
		#lista_materias = AlumnoMateria.objects.list_materias_cursando(request.user).order_by('state')
		lista_materias = PlanMateria.objects.list_materias_cursando(request.user, plancarrera)
		dict_data['th_estado'] = _(u' Estado ')
	elif dict_data['tab_selected'] == 'para_cursar':
		# Busco las que no tienen correlativas pendientes y no están en AlumnoMateria
		lista_materias = PlanMateria.objects.list_materias_para_cursar(request.user, plancarrera)
		dict_data['th_estado'] = _(u' ')
	elif dict_data['tab_selected'] == 'faltan_correl':
		# Busco las que tienen correlativas pendientes y no están en AlumnoMateria
		lista_materias = PlanMateria.objects.list_materias_faltan_correl(request.user, plancarrera)
		# dict_data['th_estado'] = _(u' ')
	elif dict_data['tab_selected'] == 'aprobadas':
		# Busco las que están en  AlumnoMateria y aprobadas
		#lista_materias = AlumnoMateria.objects.list_materias_aprobadas(request.user)
		lista_materias = PlanMateria.objects.list_materias_aprobadas(request.user, plancarrera)
		dict_data['th_estado'] = _(u' Aprobada ')
		dict_data['th_correlativas'] = _(u' Nota ')
	elif dict_data['tab_selected'] == 'todas':
		lista_materias = PlanMateria.objects.filter(plancarrera=plancarrera).order_by('cuatrimestre', 'materia')
		lista_materias_a_cursar = PlanMateria.objects.list_materias_para_cursar(request.user, plancarrera)		
		dict_data['lista_materias_a_cursar'] = lista_materias_a_cursar
		dict_data['th_estado'] = _(u' Estado ')
		dict_data['th_correlativas'] = _(u' Correlativas ')
	else:
		raise Http404(_('Error 404'))

	dict_data['lista_materias'] = lista_materias
	return render_to_response('facultad/plancarrera.html', dict_data,
							  context_instance=RequestContext(request))

def _get_correlativas(lista_materias, plancarrera):
	new_list = []
	for m in lista_materias:
		l = PlanMateria.objects.filter(plancarrera=plancarrera, materia=m.materia)
		if l.count() > 0:
			m.cuatrimestre = l[0].cuatrimestre
			new_list.append(m)
	return new_list
"""
	try:
		# Calcular cuándo se cursan
		list_correl = {}
		l = {}
		for pc in dict_data['lista_materias']:
			# Initial
			materia = pc.materia
			if not l.has_key(materia.codigo):
				l[materia.codigo] = 1
			list_correlativas = Correlativa.objects.filter(materia=pc)
			list_correl[materia.codigo] =  []
			for c in list_correlativas:
				try:
					list_correl[materia.codigo].append(c.correlativa.materia)
				except:
					import sys
					print sys.exc_info()[0]
					continue
			for c in list_correlativas:
				try:
					mmcc = MateriaCursada.objects.get(user=request.user, materia=c.correlativa.materia)
					if not mmcc.final():
						list_correl[materia.codigo].append(c.correlativa.materia)
						if mmcc.cursando():
							l[mmcc.materia.codigo] = 0
						elif mmcc.aprobada():
							l[mmcc.materia.codigo] = -1
					else:
						l[mmcc.materia.codigo] = -2
				except ObjecthoesNotExist:
					list_correl[materia.codigo].append(c.correlativa.materia)
					continue
			list_cuat = []
			for c in list_correl[materia.codigo]:
				list_cuat.append(l[c.codigo])
			if list_cuat:
				l[materia.codigo] = max(list_cuat) + 1
		dict_data['list_falta_cuat'] = l
		dict_data['list_correl'] = list_correl
	except ObjecthoesNotExist:
		# Redirect to main carrera.
		alumno = Alumno.objects.get_main_carrera(user=request.user)
		return HttpResponseRedirect(alumno.url_materias())
	form = forms.MateriasFilterForm()
	dict_data['form'] = form
	return render_to_response('plan_materias.html', dict_data,
							  context_instance=RequestContext(request))
"""

@login_required
@get_carreras
def materia(request, codigo):
	dict_data['list_carreras'] = request.session.get('list_carreras', list())
	materia = get_object_or_404(Materia, id=codigo)

	if request.method == 'POST':
		form = CursadaForm(request.POST)
		if form.is_valid():
			form.save(request.user, materia)
			AlumnoMateria.objects.update_creditos(request.user, dict_data['list_carreras'])
			request.user.message_set.create(message=_('Cambios guardados.'))
			logger.info("%s - facultadmateria: user '%s', materia '%s', state '%s', form %s" % (request.META.get('REMOTE_ADDR'), request.user, codigo, form.cleaned_data['state'], form.cleaned_data))
			if request.session.has_key('plancarrera'):
				return HttpResponseRedirect(reverse('facultad-materias-carrera', args=[request.session.get('plancarrera')]))
	else:
		initial_data = AlumnoMateria.objects.get_initial_data(request.user, materia)
		form = CursadaForm(initial=initial_data)
		#request.session.set('redirect_url', request.META.get('HTTP_REFERER', ''))
	# form.fields['materia_curso'].choices = [('-', 'Curso')] + [(c.id, c.docentes) for c in MateriaCurso.objects.filter(pub_date='2008-03-01', materia=materia)]
	# print dir(form.fields['materia_curso']) #.fields['materia_curso']
	# MATERIA_CURSOS = [('-', '-')] + [(c.id, c.docentes) for c in MateriaCurso.objects.filter(pub_date='2008-03-01', materia=)]
	dict_data.update({ 'form' : form, 'materia' : materia, })
	return render_to_response('facultad/materia_form.html', dict_data,
							  context_instance=RequestContext(request))

def _menu_materias(GET):
	# Tab selected
	tab_sel = GET.get('show', 'cursando')
	class_sel = { tab_sel : ' class="selected"' }

	result = {
		'tab_selected'		: tab_sel,
		'class_cursando'	  : class_sel.get('cursando', ''),
		'class_para_cursar'   : class_sel.get('para_cursar', ''),
		#'class_faltan_correl' : class_sel.get('faltan_correl', ''),
		'class_aprobadas'	 : class_sel.get('aprobadas', ''),
		'class_todas'		 : class_sel.get('todas', ''),
	}
	return result

@login_required
@get_carreras
def events_add(request):
	"""
	dict_data['list_carreras'] = request.session.get('list_carreras', list())
	if request.method == 'POST':
		form = CreateEventMateriaForm(request.POST)
		form.get_initial_data(request.user)
		if form.is_valid():
			materia = get_object_or_404(Materia, id=form.cleaned_data['cod_materia'])
			title = form.cleaned_data['title']
			where = form.cleaned_data['where']
			description = form.cleaned_data['description']
			date_event = form.cleaned_data['date_event']
			event = Event.objects.create(title=title, where=where, description=description, date=date_event)
			EventMateria.objects.create(event=event, user=request.user, materia=materia)
			request.user.message_set.create(message=_('Fecha agregada.'))
			logger.info("%s - facultad-events_add: id %s, user '%s', materia '%s', '%s', '%s', '%s', '%s'" %
				(request.META.get('REMOTE_ADDR'), event.id, request.user, materia.id, title, where, date_event, description))
		else:
			logger.error("%s - facultad-events_add: user '%s', materia '%s', title '%s', where '%s', date_event '%s/%s/%s %s:%s', description '%s'" %
				(request.META.get('REMOTE_ADDR'), request.user, form.data['cod_materia'], form.data['title'], form.data['where'],
				 form.data['date_day'], form.data['date_month'], form.data['date_year'], form.data['time_hour'],
				 form.data['time_minute'], form.data['description']))
	else:
		form = CreateEventMateriaForm()
		form.get_initial_data(request.user)
	dict_data['form'] = form
	"""
	return render_to_response('materias_events_add_form.html', dict_data,
							  context_instance=RequestContext(request))

@login_required
@get_carreras
def events(request):
	dict_data['list_carreras'] = request.session.get('list_carreras', list())
	dict_data['list_carreras'] = request.session.get('list_carreras', list())
	#dict_data['event_list'] = EventMateria.objects.list_event_materia_cursando(request.user)
	return render_to_response('facultad/events.html', dict_data,
							  context_instance=RequestContext(request))


@login_required
@get_carreras
def cargar_materias(request):
	dict_data['list_carreras'] = request.session.get('list_carreras', list())
	if request.method == 'POST':
		dict_result = sist_acad.parse_materias_aprobadas(request.POST['paste'], request)
		AlumnoMateria.objects.update_creditos(request.user, dict_data['list_carreras'])
		dict_data.update(dict_result)
	else:
		# Clean cache!
		dict_data.update({ 'text_paste' : '', 'materia_list' : '', 'notfound_list' : '' })
	return render_to_response('facultad/cargar_materias.html', dict_data,
							  context_instance=RequestContext(request))

