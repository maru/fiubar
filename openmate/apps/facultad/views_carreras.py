# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.cache import cache
from facultad.models import Carrera, Alumno, AlumnoMateria, PlanCarrera
from facultad import forms
from facultad.decorators import get_carreras
from django.views.generic import list_detail
from openmate.core.log import logger

dict_data = {}

@login_required
@get_carreras
def home(request):
	dict_data['list_carreras'] = request.session.get('list_carreras', list())
	return render_to_response('carreras/carreras_home.html', dict_data,
							  context_instance=RequestContext(request))

@login_required
@get_carreras
def add(request):
	dict_data['list_carreras'] = request.session.get('list_carreras', list())
	if request.method == 'POST':
		form = forms.SelectCarreraForm(request.POST)
		if form.is_valid():
			plancarrera = PlanCarrera.objects.get(id=form.cleaned_data['plancarrera'])
			begin_date = form.cleaned_data['begin_date']
			alumno = Alumno.objects.create(user=request.user, carrera=plancarrera.carrera,
					   plancarrera=plancarrera, begin_date=begin_date)
			if alumno:
				AlumnoMateria.objects.update_creditos(request.user, [alumno])
				request.user.message_set.create(message=_('Carrera agregada.'))
				logger.info("%s - carreras-add: user '%s', plancarrera '%s'" % (request.META.get('REMOTE_ADDR'), request.user, plancarrera.name))
			else:
				request.user.message_set.create(message=_(u'Ya cursás esa carrera.'))
				logger.error("%s - carreras-add: user '%s', plancarrera '%s', \"Ya cursás esa carrera.\"" % (request.META.get('REMOTE_ADDR'), request.user, plancarrera.name))
			return HttpResponseRedirect(reverse('carreras-home'))
		else:
			logger.error("%s - carreras-add: user '%s', plancarrera '%s', \"Form not valid.\"" % (request.META.get('REMOTE_ADDR'), request.user, form.cleaned_data['plancarrera']))

	form = forms.SelectCarreraForm()
	dict_data['form'] = form
	return render_to_response('carreras/carrera_add_form.html', dict_data,
							  context_instance=RequestContext(request))
@login_required
@get_carreras
def delete(request, plancarrera=None):
	if plancarrera:
		alumno = get_object_or_404(Alumno, user=request.user, plancarrera__short_name=plancarrera)
		alumno.delete()
		request.user.message_set.create(message=_('Carrera borrada.'))
		logger.info("%s - carreras-delete: user '%s', plancarrera '%s'" % (request.META.get('REMOTE_ADDR'), request.user, plancarrera))
		return HttpResponseRedirect(reverse('carreras-home'))
	# Show list of carreras
	dict_data['list_carreras'] = request.session.get('list_carreras', list())
	return render_to_response('carreras/carrera_delete.html', dict_data,
							  context_instance=RequestContext(request))

@login_required
@get_carreras
def graduado(request, plancarrera):
	dict_data['list_carreras'] = request.session.get('list_carreras', list())
	alumno = get_object_or_404(Alumno, user=request.user, plancarrera__short_name=plancarrera)
	if request.method == 'POST':
		form = forms.GraduadoForm(request.POST)
		if form.is_valid():
			alumno.graduado_date = form.cleaned_data['graduado_date']
			alumno.save()
			request.user.message_set.create(message=_(u'¡Felicitaciones!'))
			logger.info("%s - carreras-graduado: user '%s', plancarrera '%s'" % (request.META.get('REMOTE_ADDR'), request.user, alumno.plancarrera))
			return HttpResponseRedirect(reverse('carreras-home'))
	else:
		# Initial data
		initial_data = { 'plancarrera' : alumno.plancarrera.short_name }
		if alumno.graduado_date:
			initial_data['month'] = alumno.graduado_date.month
			initial_data['year'] = alumno.graduado_date.year
		form = forms.GraduadoForm(initial=initial_data)

	dict_data['form'] = form
	dict_data['alumno'] = alumno
	return render_to_response('carreras/carrera_graduado_form.html', dict_data,
							  context_instance=RequestContext(request))

@login_required
@get_carreras
def del_graduado(request, plancarrera):
	alumno = get_object_or_404(Alumno, user=request.user, plancarrera__short_name=plancarrera)
	alumno.del_graduado()
	request.user.message_set.create(message=_('A seguir estudiando...'))
	return HttpResponseRedirect(reverse('carreras-home'))

RESULTS_PER_PAGE = 10
@login_required
@get_carreras
def alumnos(request, plancarrera):
	dict_data['list_carreras'] = request.session.get('list_carreras', list())
	plancarrera = get_object_or_404(PlanCarrera, short_name=plancarrera)
	page = int(request.GET.get('p', 1))
	queryset = Alumno.objects.filter(plancarrera=plancarrera).order_by('-begin_date', '-id')
	dict_data.update({ 'plancarrera' : plancarrera, 'object' : _(u'alumno') })
	return list_detail.object_list( request, queryset=queryset,
				paginate_by=RESULTS_PER_PAGE, page=page,
				extra_context=dict_data, template_name = 'carreras/carrera_alumnos.html',
			)
