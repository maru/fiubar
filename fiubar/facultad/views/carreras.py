# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.translation import ugettext as _

from .. import forms
from fiubar.alumnos.decorators import get_carreras
from fiubar.alumnos.models import Materia as AlumnoMateria
from fiubar.alumnos.models import PlanCarrera as Alumno

from fiubar.core.log import logger


context = {'slug': 'facultad'}


@login_required
@get_carreras
def home(request):
    context['list_carreras'] = request.session.get('list_carreras', list())
    request.session['list_carreras'] = []
    return render(request, 'carreras/carreras_home.html', context)


@login_required
@get_carreras
def add(request):
    context['list_carreras'] = request.session.get('list_carreras', list())
    request.session['list_carreras'] = []
    if request.method == 'POST':
        form = forms.SelectCarreraForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            plancarrera = form.cleaned_data['plancarrera']
            begin_date = form.cleaned_data['begin_date']
            alumno = Alumno.objects.create(user=request.user,
                                           carrera=plancarrera.carrera,
                                           plancarrera=plancarrera,
                                           begin_date=begin_date)
            if alumno:
                AlumnoMateria.objects.update_creditos(request.user, [alumno])
                messages.add_message(request, messages.SUCCESS,
                                     _('Carrera agregada.'))
                logger.info("%s - carreras-add: user '%s', plancarrera '%s'" %
                            (request.META.get('REMOTE_ADDR'), request.user,
                             plancarrera.name))
            else:
                messages.add_message(request, messages.ERROR,
                                     _('Ya cursás esa carrera.'))
                logger.error("%s - carreras-add: user '%s', plancarrera '%s', "
                             '"Ya cursás esa carrera."' %
                             (request.META.get('REMOTE_ADDR'),
                              request.user, plancarrera.name))
            return HttpResponseRedirect(reverse('facultad:carreras-home'))
        else:
            logger.error("%s - carreras-add: user '%s', plancarrera '%s', "
                         '"Form not valid."' %
                         (request.META.get('REMOTE_ADDR'), request.user,
                          form.cleaned_data['plancarrera']))

    form = forms.SelectCarreraForm()
    context['form'] = form
    return render(request, 'carreras/carrera_add_form.html', context)


@login_required
@get_carreras
def delete(request, plancarrera=None):
    context['list_carreras'] = request.session.get('list_carreras', list())
    request.session['list_carreras'] = []
    if plancarrera:
        alumno = get_object_or_404(Alumno, user=request.user,
                                   plancarrera__short_name=plancarrera)
        alumno.delete()
        messages.add_message(request, messages.SUCCESS, _('Carrera borrada.'))
        logger.info("%s - carreras-delete: user '%s', plancarrera '%s'" %
                    (request.META.get('REMOTE_ADDR'),
                     request.user, plancarrera))
        return HttpResponseRedirect(reverse('facultad:carreras-home'))
    # Show list of carreras
    return render(request, 'carreras/carrera_delete.html', context)


@login_required
@get_carreras
def graduado(request, plancarrera):
    context['list_carreras'] = request.session.get('list_carreras', list())
    request.session['list_carreras'] = []
    alumno = get_object_or_404(Alumno, user=request.user,
                               plancarrera__short_name=plancarrera)
    if request.method == 'POST':
        form = forms.GraduadoForm(request.POST)
        if form.is_valid():
            alumno.graduado_date = form.cleaned_data['graduado_date']
            alumno.save()
            messages.add_message(request, messages.SUCCESS,
                                 _('¡Felicitaciones!'))
            logger.info("%s - carreras-graduado: user '%s', plancarrera '%s'" %
                        (request.META.get('REMOTE_ADDR'),
                         request.user, alumno.plancarrera))
            return HttpResponseRedirect(reverse('facultad:carreras-home'))
    else:
        # Initial data
        initial_data = {'plancarrera': alumno.plancarrera.short_name}
        if alumno.graduado_date:
            initial_data['month'] = alumno.graduado_date.month
            initial_data['year'] = alumno.graduado_date.year
        form = forms.GraduadoForm(initial=initial_data)

    context['form'] = form
    context['alumno'] = alumno
    return render(request, 'carreras/carrera_graduado_form.html', context)


@login_required
def del_graduado(request, plancarrera):
    alumno = get_object_or_404(Alumno, user=request.user,
                               plancarrera__short_name=plancarrera)
    alumno.del_graduado()
    messages.add_message(request, messages.INFO, _('A seguir estudiando...'))
    return HttpResponseRedirect(reverse('facultad:carreras-home'))
