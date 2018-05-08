# -*- coding: utf-8 -*-
import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView

from . import sist_acad
from .. import forms
from ..decorators import get_carreras
from ..models import Alumno, AlumnoMateria, Materia, PlanMateria


# Get an instance of a logger
logger = logging.getLogger('fiubar')

context = {'slug': 'facultad'}


class HomePageView(TemplateView):

    template_name = "facultad/home.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Materias cursadas
        context['list_matcur'] = AlumnoMateria.objects\
            .list_materias_cursando(self.request.user)
        return context

class PlanCarreraView(TemplateView):

    template_name = "facultad/plancarrera.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        plancarrera = kwargs['plancarrera']
        user = self.request.user

        # Get carrera y plan
        alumno = get_object_or_404(Alumno,
                                   plancarrera__short_name=plancarrera,
                                   user=user)
        context['carrera'] = alumno.carrera
        plancarrera = alumno.plancarrera
        context['plancarrera'] = plancarrera

        # Menu
        context.update(_menu_materias(self.request.GET))
        context['th_correlativas'] = _(' ')
        # Materias
        if context['tab_selected'] == 'cursando':
            # Busco las que están en  AlumnoMateria y no aprobadas
            lista_materias = PlanMateria.objects\
                .list_materias_cursando(user, plancarrera)
            context['th_estado'] = _(' Estado ')
        elif context['tab_selected'] == 'para_cursar':
            # No tienen correlativas pendientes y no están en AlumnoMateria
            lista_materias = PlanMateria.objects\
                .list_materias_para_cursar(user, plancarrera)
            context['th_estado'] = _(' ')
        elif context['tab_selected'] == 'faltan_correl':
            # Tienen correlativas pendientes y no están en AlumnoMateria
            lista_materias = PlanMateria.objects\
                .list_materias_faltan_correl(user, plancarrera)
            # context['th_estado'] = _(' ')
        elif context['tab_selected'] == 'aprobadas':
            # Busco las que están en  AlumnoMateria y aprobadas
            lista_materias = PlanMateria.objects\
                .list_materias_aprobadas(user, plancarrera)
            context['th_estado'] = _(' Aprobada ')
            context['th_correlativas'] = _(' Nota ')
        elif context['tab_selected'] == 'todas':
            lista_materias = PlanMateria.objects\
                .filter(plancarrera=plancarrera).order_by('cuatrimestre',
                                                          'materia')
            lista_materias_a_cursar = PlanMateria.objects\
                .list_materias_para_cursar(user, plancarrera)
            context['lista_materias_a_cursar'] = lista_materias_a_cursar
            context['th_estado'] = _(' Estado ')
            context['th_correlativas'] = _(' Correlativas ')
        else:
            raise Http404(_('Error 404'))

        context['lista_materias'] = lista_materias
        return context


def _get_correlativas(lista_materias, plancarrera):
    new_list = []
    for m in lista_materias:
        mat = PlanMateria.objects.filter(plancarrera=plancarrera,
                                         materia=m.materia)
        if mat.count() > 0:
            m.cuatrimestre = mat[0].cuatrimestre
            new_list.append(m)
    return new_list


@login_required
@get_carreras
def materia(request, codigo):
    materia = get_object_or_404(Materia, id=codigo)

    if request.method == 'POST':
        form = forms.CursadaForm(request.POST)
        if form.is_valid():
            form.save(request.user, materia)
            AlumnoMateria.objects.update_creditos(request.user,
                                                  context['list_carreras'])
            messages.add_message(request, messages.SUCCESS,
                                 _('Cambios guardados.'))
            logger.info("%s - facultadmateria: user '%s', materia '%s', "
                        "state '%s', form %s" %
                        (request.META.get('REMOTE_ADDR'), request.user, codigo,
                         form.cleaned_data['state'], form.cleaned_data))
            if 'plancarrera' in request.session:
                return HttpResponseRedirect(
                    reverse('facultad:materias-carrera',
                            args=[request.session.get('plancarrera')]))
    else:
        initial_data = AlumnoMateria.objects\
            .get_initial_data(request.user, materia)
        form = forms.CursadaForm(initial=initial_data)
    context.update({'form': form, 'materia': materia})
    return render(request, 'facultad/materia_form.html', context)


def _menu_materias(GET):
    # Tab selected
    tab_sel = GET.get('show', 'cursando')
    class_sel = {tab_sel: ' class="selected"'}

    result = {
        'tab_selected': tab_sel,
        'class_cursando': class_sel.get('cursando', ''),
        'class_para_cursar': class_sel.get('para_cursar', ''),
        'class_aprobadas': class_sel.get('aprobadas', ''),
        'class_todas': class_sel.get('todas', ''),
    }
    return result


@login_required
@get_carreras
def cargar_materias(request):
    if request.method == 'POST':
        dict_result = sist_acad.parse_materias_aprobadas(request.POST['paste'],
                                                         request)
        AlumnoMateria.objects.update_creditos(request.user,
                                              context['list_carreras'])
        context.update(dict_result)
    else:
        # Clean cache!
        context.update({'text_paste': '',
                        'materia_list': '',
                        'notfound_list': ''})
    return render(request, 'facultad/cargar_materias.html', context)
