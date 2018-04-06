# -*- coding: utf-8 -*-
import datetime

from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from django.urls import reverse
from django.contrib import messages

from fiubar.core.log import logger

from ..models.models import PlanMateria, Alumno, Carrera, AlumnoMateria, Materia
from ..decorators import get_carreras
from .. import forms
from . import sist_acad
#from event.forms import CreateEventMateriaForm
#from event.models import EventMateria, Event

context = {'slug': 'facultad'}

@login_required
@get_carreras
def home(request):
    # Carreras and Materias
    context['list_carreras'] = request.session.get('list_carreras', list())
    request.session['list_carreras'] = []
    context['list_matcur'] = AlumnoMateria.objects.get_summary(request.user)
    return render(request, 'facultad/home.html', context)

@login_required
@get_carreras
def plancarrera_all(request):
    context['list_carreras'] = request.session.get('list_carreras', list())
    request.session['list_carreras'] = []
    # Menu
    context.update(_menu_materias(request.GET))
    context['th_correlativas'] = _(u' ')
    # Materias
    if context['tab_selected'] == 'cursando':
        # Busco las que están en  AlumnoMateria y no aprobadas
        lista_materias = AlumnoMateria.objects.list_materias_cursando(request.user).order_by('state')
        context['th_estado'] = _(u'Estado')
    elif context['tab_selected'] == 'aprobadas':
        # Busco las que están en  AlumnoMateria y aprobadas
        lista_materias = AlumnoMateria.objects.list_materias_aprobadas(request.user)
        context['th_estado'] = _(u'Aprobada')
        context['th_correlativas'] = u'Nota '
    else:
        raise Http404(_('Error 404'))

    context['lista_materias'] = lista_materias
    return render(request, 'facultad/plancarrera_all.html', context)

@login_required
@get_carreras
def plancarrera(request, plancarrera):
    context['list_carreras'] = request.session.get('list_carreras', list())
    request.session['list_carreras'] = []

    # Get carrera y plan
    alumno = get_object_or_404(Alumno, plancarrera__short_name=plancarrera, user=request.user)
    context['carrera'] = alumno.carrera
    plancarrera = alumno.plancarrera
    context['plancarrera'] = plancarrera

    # Menu
    context.update(_menu_materias(request.GET))
    context['th_correlativas'] = _(u' ')
    # Materias
    if context['tab_selected'] == 'cursando':
        # Busco las que están en  AlumnoMateria y no aprobadas
        #lista_materias = AlumnoMateria.objects.list_materias_cursando(request.user).order_by('state')
        lista_materias = PlanMateria.objects.list_materias_cursando(request.user, plancarrera)
        context['th_estado'] = _(u' Estado ')
    elif context['tab_selected'] == 'para_cursar':
        # Busco las que no tienen correlativas pendientes y no están en AlumnoMateria
        lista_materias = PlanMateria.objects.list_materias_para_cursar(request.user, plancarrera)
        context['th_estado'] = _(u' ')
    elif context['tab_selected'] == 'faltan_correl':
        # Busco las que tienen correlativas pendientes y no están en AlumnoMateria
        lista_materias = PlanMateria.objects.list_materias_faltan_correl(request.user, plancarrera)
        # context['th_estado'] = _(u' ')
    elif context['tab_selected'] == 'aprobadas':
        # Busco las que están en  AlumnoMateria y aprobadas
        #lista_materias = AlumnoMateria.objects.list_materias_aprobadas(request.user)
        lista_materias = PlanMateria.objects.list_materias_aprobadas(request.user, plancarrera)
        context['th_estado'] = _(u' Aprobada ')
        context['th_correlativas'] = _(u' Nota ')
    elif context['tab_selected'] == 'todas':
        lista_materias = PlanMateria.objects.filter(plancarrera=plancarrera).order_by('cuatrimestre', 'materia')
        lista_materias_a_cursar = PlanMateria.objects.list_materias_para_cursar(request.user, plancarrera)
        context['lista_materias_a_cursar'] = lista_materias_a_cursar
        context['th_estado'] = _(u' Estado ')
        context['th_correlativas'] = _(u' Correlativas ')
    else:
        raise Http404(_('Error 404'))

    context['lista_materias'] = lista_materias
    return render(request, 'facultad/plancarrera.html', context)

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
        for pc in context['lista_materias']:
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
        context['list_falta_cuat'] = l
        context['list_correl'] = list_correl
    except ObjecthoesNotExist:
        # Redirect to main carrera.
        alumno = Alumno.objects.get_main_carrera(user=request.user)
        return HttpResponseRedirect(alumno.url_materias())
    form = forms.MateriasFilterForm()
    context['form'] = form
    return render(request, 'plan_materias.html', context)
"""

@login_required
@get_carreras
def materia(request, codigo):
    context['list_carreras'] = request.session.get('list_carreras', list())
    request.session['list_carreras'] = []
    materia = get_object_or_404(Materia, id=codigo)

    if request.method == 'POST':
        form = forms.CursadaForm(request.POST)
        if form.is_valid():
            form.save(request.user, materia)
            AlumnoMateria.objects.update_creditos(request.user, context['list_carreras'])
            messages.add_message(request, messages.SUCCESS, _('Cambios guardados.'))
            logger.info("%s - facultadmateria: user '%s', materia '%s', state '%s', form %s" % (request.META.get('REMOTE_ADDR'), request.user, codigo, form.cleaned_data['state'], form.cleaned_data))
            if request.session.has_key('plancarrera'):
                return HttpResponseRedirect(reverse('facultad:facultad:facultad-materias-carrera', args=[request.session.get('plancarrera')]))
    else:
        initial_data = AlumnoMateria.objects.get_initial_data(request.user, materia)
        form = forms.CursadaForm(initial=initial_data)
        #request.session.set('redirect_url', request.META.get('HTTP_REFERER', ''))
    context.update({ 'form' : form, 'materia' : materia, })
    return render(request, 'facultad/materia_form.html', context)

def _menu_materias(GET):
    # Tab selected
    tab_sel = GET.get('show', 'cursando')
    class_sel = { tab_sel : ' class="selected"' }

    result = {
        'tab_selected'        : tab_sel,
        'class_cursando'      : class_sel.get('cursando', ''),
        'class_para_cursar'   : class_sel.get('para_cursar', ''),
        #'class_faltan_correl' : class_sel.get('faltan_correl', ''),
        'class_aprobadas'     : class_sel.get('aprobadas', ''),
        'class_todas'         : class_sel.get('todas', ''),
    }
    return result

@login_required
@get_carreras
def events_add(request):
    """
    context['list_carreras'] = request.session.get('list_carreras', list())
    request.session['list_carreras'] = []
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
            messages.add_message(request, messages.SUCCESS, _('Fecha agregada.'))
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
    context['form'] = form
    """
    return render(request, 'materias_events_add_form.html', context)

@login_required
@get_carreras
def events(request):
    context['list_carreras'] = request.session.get('list_carreras', list())
    request.session['list_carreras'] = []
    #context['event_list'] = EventMateria.objects.list_event_materia_cursando(request.user)
    return render(request, 'facultad/events.html', context)


@login_required
@get_carreras
def cargar_materias(request):
    context['list_carreras'] = request.session.get('list_carreras', list())
    request.session['list_carreras'] = []
    if request.method == 'POST':
        dict_result = sist_acad.parse_materias_aprobadas(request.POST['paste'], request)
        AlumnoMateria.objects.update_creditos(request.user, context['list_carreras'])
        context.update(dict_result)
    else:
        # Clean cache!
        context.update({ 'text_paste' : '', 'materia_list' : '', 'notfound_list' : '' })
    return render(request, 'facultad/cargar_materias.html', context)
