# -*- coding: utf-8 -*-
import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext as _
from django.views.generic.base import RedirectView, TemplateView
from django.views.generic.edit import FormView

from ..forms import GraduadoForm, SelectCarreraForm
from ..models import Alumno


# Get an instance of a logger
logger = logging.getLogger('fiubar')

context = {'slug': 'facultad'}


class HomePageView(LoginRequiredMixin, TemplateView):

    template_name = "carreras/carreras_home.html"


class AddView(LoginRequiredMixin, FormView):

    template_name = "carreras/carrera_add_form.html"
    form_class = SelectCarreraForm

    def form_valid(self, form):
        request = self.request
        plancarrera = form.cleaned_data['plancarrera']
        begin_date = form.cleaned_data['begin_date']
        alumno = Alumno.objects.create(user=request.user,
                                       carrera=plancarrera.carrera,
                                       plancarrera=plancarrera,
                                       begin_date=begin_date)
        if alumno:
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

    def form_invalid(self, form):

        logger.error("%s - carreras-add: user '%s', plancarrera '%s', "
                     '"Form not valid."' %
                     (self.request.META.get('REMOTE_ADDR'), self.request.user,
                      form.cleaned_data.get('plancarrera')))

        return super(AddView, self).form_invalid(form)


class DeleteView(LoginRequiredMixin, TemplateView):

    template_name = "carreras/carrera_delete.html"

    def get(self, request, *args, **kwargs):
        plancarrera = kwargs.get('plancarrera')

        if plancarrera:
            alumno = get_object_or_404(Alumno, user=request.user,
                                       plancarrera__short_name=plancarrera)
            alumno.delete()
            messages.add_message(request, messages.SUCCESS,
                                 _('Carrera borrada.'))

            logger.info("%s - carreras-delete: user '%s', plancarrera '%s'" %
                        (request.META.get('REMOTE_ADDR'),
                         request.user, plancarrera))

            return HttpResponseRedirect(reverse('facultad:carreras-home'))

        return super().get(request, *args, **kwargs)


class GraduadoView(LoginRequiredMixin, FormView):

    template_name = "carreras/carrera_graduado_form.html"
    form_class = GraduadoForm
    success_url = reverse_lazy('facultad:carreras-home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['alumno'] = self.alumno
        return context

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super(GraduadoView, self).get_initial()

        self.plan_carrera = self.kwargs['plancarrera']
        initial['plancarrera'] = self.plan_carrera

        alumno = get_object_or_404(Alumno, user=self.request.user,
                                   plancarrera__short_name=self.plan_carrera)
        self.alumno = alumno

        if alumno.graduado_date:
            initial['month'] = alumno.graduado_date.month
            initial['year'] = alumno.graduado_date.year

        return initial

    def form_valid(self, form):
        alumno = get_object_or_404(Alumno, user=self.request.user,
                                   plancarrera__short_name=self.plan_carrera)
        alumno.graduado_date = form.cleaned_data['graduado_date']
        alumno.save()

        messages.add_message(self.request, messages.SUCCESS,
                             _('¡Felicitaciones!'))

        logger.info("%s - carreras-graduado: user '%s', plancarrera '%s'" %
                    (self.request.META.get('REMOTE_ADDR'),
                     self.request.user, alumno.plancarrera))

        return super(GraduadoView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        try:
            return super(GraduadoView, self).post(request, *args, **kwargs)
        except ValidationError as e:
            form = self.get_form()
            messages.add_message(self.request, messages.ERROR, e.messages[0])
            return self.form_invalid(form)


class GraduadoDeleteView(LoginRequiredMixin, RedirectView):

    url = reverse_lazy('facultad:carreras-home')

    def get(self, request, *args, **kwargs):
        plancarrera = kwargs.get('plancarrera')

        alumno = get_object_or_404(Alumno, user=request.user,
                                   plancarrera__short_name=plancarrera)
        alumno.del_graduado()

        messages.add_message(request, messages.INFO,
                             _('A seguir estudiando...'))

        return super(GraduadoDeleteView, self).get(request, args, kwargs)
