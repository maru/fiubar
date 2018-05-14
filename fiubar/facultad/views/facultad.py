# -*- coding: utf-8 -*-
import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from ..forms import CursadaForm
from ..models import Alumno, AlumnoMateria, Materia, PlanMateria
from .sist_acad import parse_materias_aprobadas


# Get an instance of a logger
logger = logging.getLogger('fiubar')

context = {'slug': 'facultad'}


class HomePageView(LoginRequiredMixin, TemplateView):

    template_name = "facultad/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Materias cursadas
        context['list_matcur'] = AlumnoMateria.objects\
            .list_materias_cursando(self.request.user)
        return context


class PlanCarreraView(LoginRequiredMixin, TemplateView):

    template_name = "facultad/plancarrera.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

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
            from django.http import Http404
            raise Http404(_('Error 404'))

        context['lista_materias'] = lista_materias
        return context


class MateriaView(LoginRequiredMixin, FormView):

    template_name = "facultad/materia_form.html"
    form_class = CursadaForm
    materia = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['materia'] = self.materia
        return context

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super(MateriaView, self).get_initial()

        codigo = self.kwargs['codigo']
        self.materia = get_object_or_404(Materia, id=codigo)

        initial.update(AlumnoMateria.objects.
                       get_initial_data(self.request.user, self.materia))
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save(self.request.user, self.materia)

        AlumnoMateria.objects.update_creditos(self.request.user)
        messages.add_message(self.request, messages.SUCCESS,
                             _('Cambios guardados.'))
        logger.info("%s - facultadmateria: user '%s', materia '%s', "
                    "state '%s', form %s" %
                    (self.request.META.get('REMOTE_ADDR'), self.request.user,
                     self.materia.id, form.cleaned_data['state'],
                     form.cleaned_data))

        return super(MateriaView, self).form_valid(form)

    def get_success_url(self):
        codigo = self.kwargs['codigo']
        return reverse('facultad:materia', args=[codigo])


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


class CargarMateriasView(LoginRequiredMixin, TemplateView):

    template_name = "facultad/cargar_materias.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        # print(self.kwargs)
        # print(context)
        dict_result = parse_materias_aprobadas(request.user,
                                               request.POST.get('text_paste'),
                                               request.META.get('REMOTE_ADDR'))
        AlumnoMateria.objects.update_creditos(request.user)
        context.update(dict_result)
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        # Clean cache!
        context = self.get_context_data(**kwargs)
        context.update({'text_paste': '',
                        'materia_list': '',
                        'materia_list_count': 0})
        return self.render_to_response(context)
