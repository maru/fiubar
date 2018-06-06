# -*- coding: utf-8 -*-
import json
import logging

from allauth.account.forms import LoginForm, SignupForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView

from fiubar.facultad.models import Alumno, AlumnoMateria, Materia, PlanCarrera


logger = logging.getLogger('fiubar')


class HomePageView(TemplateView):

    template_name = "new_user/index.html"

    def cargar_carrera(self, request):
        try:
            pc = json.loads(request.COOKIES.get('plancarrera', '{}'))
            plancarrera = PlanCarrera.objects.get(id=pc.get('id'))
            alumno = Alumno.objects.create(user=request.user,
                                           carrera=plancarrera.carrera,
                                           plancarrera=plancarrera)
            if alumno:
                messages.add_message(request, messages.SUCCESS,
                                     _('Carrera agregada.'))
                logger.info("%s - carreras-add: user '%s', "
                            "plancarrera '%s'" %
                            (request.META.get('REMOTE_ADDR'), request.user,
                             plancarrera.name))
        except Exception as e:
            logger.error("%s - carreras-add: user '%s', plancarrera '%s',"
                         "exception: %s" %
                         (request.META.get('REMOTE_ADDR'), request.user,
                          pc, e.args[0]))

    def cargar_materias(self, request):
        materias = json.loads(request.COOKIES.get('materias', '{}'))
        count_materias = 0
        for m in materias:
            try:
                materia = Materia.objects.get(id=m[1]['materia'])
                estado = m[1]['estado']
                obj, created = AlumnoMateria.objects.update_or_create(
                    user=request.user, materia=materia,
                    defaults={'state': estado})
                logger.info("%s - facultadmateria: user '%s', "
                            "materia '%s', state '%s'" %
                            (request.META.get('REMOTE_ADDR'), request.user,
                             materia.id, estado))
                count_materias += 1
            except Exception as e:
                logger.error("%s - facultadmateria: user '%s', "
                             "materia '%s', state '%s', exception: %s" %
                             (request.META.get('REMOTE_ADDR'),
                              request.user, m[1]['materia'],
                              m[1]['estado'], e.args[0]))

        if count_materias > 0:
            AlumnoMateria.objects.update_creditos(request.user)
            msg = {False: _('Se cargó 1 materia.'),
                   True: _('Se cargaron %d materias.') % count_materias}
            messages.add_message(request, messages.SUCCESS,
                                 msg[count_materias > 1])

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and 'create_alumno'in request.COOKIES:
            # Actualizo o creo Alumno
            self.cargar_carrera(request)
            # Actualizo o creo AlumnoMateria
            self.cargar_materias(request)

        if self.request.user.is_authenticated:
            # Redireccionamos directo a la lista de materias
            response = HttpResponseRedirect(reverse('facultad:home'))
        else:
            response = super(HomePageView, self).get(request, *args, **kwargs)

        # Limpiar cookies
        for name in ['create_alumno', 'carrera', 'plancarrera', 'materias']:
            response.delete_cookie(name)

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({'slug': 'home',
                        'forms': {'login': LoginForm,
                                  'signup': SignupForm}
                        })
        return context
