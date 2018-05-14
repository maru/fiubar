import logging
from datetime import date

from django.contrib.messages import constants as MSG
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils.translation import ugettext as _

from ..models import Alumno
from .common import BaseUserTestCase


logging.disable(logging.CRITICAL)


class HomePageViewTestCase(BaseUserTestCase):

    def test_home(self):
        response = self.client.get(reverse('facultad:carreras-home'))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.template_name,
                         ['carreras/carreras_home.html'])
        self.assertContains(response, '<h3 class="panel-title">Carreras</h3>')
        self.assertContains(response,
                            '<td class="carrera">\n'
                            '                <a href="/facultad/materias/'
                            'cocky_perlman00/?show=todas"> <span></span></a>')


class AddViewTestCase(BaseUserTestCase):

    def test_add_ok(self):
        response = self.client.get(reverse('facultad:carreras-add'))
        self.assertEqual(response.status_code, 200)

    def test_add_post_invalid_empty(self):
        response = self.client.post(
            reverse('facultad:carreras-add'),
            {})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['form'].errors), 4)

    def test_add_post_invalid_empty_values(self):
        response = self.client.post(
            reverse('facultad:carreras-add'),
            {'plancarrera': '', 'begin_date': '',
             'cuatrimestre': '', 'year': ''})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['form'].errors), 4)

    def test_add_post_invalid_plancarrera(self):
        response = self.client.post(
            reverse('facultad:carreras-add'),
            {'plancarrera': '404',
             'cuatrimestre': '1', 'year': '2015'})

        self.assertEqual(response.status_code, 200)

        e = response.context['form'].errors
        self.assertEqual(len(e), 1)
        self.assertIsNotNone(e.get('plancarrera'))

    def test_add_post_invalid_date(self):
        pc = self.alumnos[1].plancarrera

        response = self.client.post(
            reverse('facultad:carreras-add'),
            {'plancarrera': pc.id,
             'cuatrimestre': 'x', 'year': '2015'})

        self.assertEqual(response.status_code, 200)

        e = response.context['form'].errors
        self.assertEqual(len(e), 2)
        self.assertIsNotNone(e.get('cuatrimestre'))
        self.assertIsNotNone(e.get('begin_date'))

    def test_add_post_invalid_new(self):
        pc = self.alumnos[1].plancarrera

        response = self.client.post(
            reverse('facultad:carreras-add'),
            {'plancarrera': pc.id,
             'cuatrimestre': '1', 'year': '2015'},
            follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain,
                         [(reverse('facultad:carreras-home'), 302)])
        self.assertEqual(response.template_name,
                         ['carreras/carreras_home.html'])

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].level, MSG.ERROR)
        self.assertEqual(messages[0].message, _('Ya cursás esa carrera.'))

    def test_add_post_valid_new(self):
        pc = self.plan_carreras[3]

        response = self.client.post(
            reverse('facultad:carreras-add'),
            {'plancarrera': pc.id,
             'cuatrimestre': '1', 'year': '2015'},
            follow=True)

        self.assertEqual(response.status_code, 200)

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].level, MSG.SUCCESS)
        self.assertEqual(messages[0].message, _('Carrera agregada.'))


class DeleteViewTestCase(BaseUserTestCase):

    def test_delete_ok(self):
        response = self.client.get(reverse('facultad:carreras-show_delete'))
        self.assertEqual(response.status_code, 200)

    def test_delete_plancarrera_ok(self):
        pc = self.alumnos[1].plancarrera

        response = self.client.get(
            reverse('facultad:carreras-delete',
                    args=[pc.short_name]),
            follow=True)

        self.assertEqual(response.status_code, 200)

        with self.assertRaises(ObjectDoesNotExist):
            Alumno.objects.get(user=self.user, plancarrera=pc)

    def test_delete_plancarrera_404(self):
        response = self.client.get(
            reverse('facultad:carreras-delete',
                    args=['404']))

        self.assertEqual(response.status_code, 404)


class GraduadoViewTestCase(BaseUserTestCase):

    def test_graduado_get_ok(self):
        pc = self.alumnos[1].plancarrera

        response = self.client.get(
            reverse('facultad:carreras-graduado',
                    args=[pc.short_name]))

        self.assertEqual(response.status_code, 200)

    def test_graduado_get_404(self):
        response = self.client.get(
            reverse('facultad:carreras-graduado',
                    args=['404']))

        self.assertEqual(response.status_code, 404)

    def test_graduado_get_graduado_ok(self):
        pc = self.alumnos[1].plancarrera

        a = Alumno.objects.get(user=self.user, plancarrera=pc)
        a.graduado_date = date(2020, 12, 13)
        a.save()

        self.assertTrue(a.is_graduado())

        response = self.client.get(
            reverse('facultad:carreras-graduado',
                    args=[pc.short_name]))

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['form'].initial,
                         {'plancarrera': 'cocky_perlman00',
                          'month': 12, 'year': 2020})

    def test_graduado_post_invalid(self):
        pc = self.alumnos[1].plancarrera

        response = self.client.post(
            reverse('facultad:carreras-graduado',
                    args=[pc.short_name]),
            {'month': 1, 'plancarrera': pc.short_name},
            follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain, [])
        self.assertEqual(response.template_name,
                         ['carreras/carrera_graduado_form.html'])

        e = response.context['form'].errors
        self.assertEqual(len(e), 2)
        self.assertIsNotNone(e.get('graduado_date'))
        self.assertIsNotNone(e.get('year'))

    def test_graduado_post_valid(self):
        pc = self.alumnos[1].plancarrera

        response = self.client.post(
            reverse('facultad:carreras-graduado',
                    args=[pc.short_name]),
            {'month': 1, 'year': 2018, 'plancarrera': pc.short_name},
            follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain,
                         [(reverse('facultad:carreras-home'), 302)])
        self.assertEqual(response.template_name,
                         ['carreras/carreras_home.html'])

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].level, MSG.SUCCESS)
        self.assertEqual(messages[0].message, _('¡Felicitaciones!'))

        a = Alumno.objects.get(user=self.user, plancarrera=pc)
        self.assertEqual(a.graduado_date, date(2018, 1, 1))


class GraduadoDeleteViewTestCase(BaseUserTestCase):

    def test_graduado_delete_ok(self):
        pc = self.alumnos[1].plancarrera

        a = Alumno.objects.get(user=self.user, plancarrera=pc)
        a.graduado_date = date(2020, 12, 13)
        a.save()

        self.assertTrue(a.is_graduado())

        response = self.client.get(
            reverse('facultad:carreras-graduado-delete',
                    args=[pc.short_name]),
            follow=True)

        self.assertEqual(response.status_code, 200)

        a = Alumno.objects.get(user=self.user, plancarrera=pc)
        self.assertFalse(a.is_graduado())

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].level, MSG.INFO)
        self.assertEqual(messages[0].message, _('A seguir estudiando...'))

    def test_graduado_delete_404(self):
        response = self.client.get(
            reverse('facultad:carreras-graduado-delete',
                    args=['angry_jang00']))

        self.assertEqual(response.status_code, 404)
