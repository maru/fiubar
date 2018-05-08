import logging
from datetime import date
from django.urls import reverse
from test_plus.test import TestCase

from ..models import (Alumno, AlumnoMateria, Carrera, Correlativa,
                      Departamento, Materia, PlanCarrera, PlanMateria)


logging.disable(logging.CRITICAL)


class BaseUserTestCase(TestCase):

    def setUp(self):
        self.user = self.make_user()

    def create_new_alumno(self):
        c = []
        c.append(Carrera.objects.create(codigo='a', abbr_name='cocky_perlman'))
        c.append(Carrera.objects.create(codigo='b', abbr_name='berserk_hamil'))
        c.append(Carrera.objects.create(codigo='c', abbr_name='angry_jang'))

        pc = []
        pc.append(PlanCarrera.objects.create(carrera=c[0],
                                             pub_date=date(2012, 1, 1),
                                             min_creditos=100,
                                             short_name='cocky_perlman12'))
        pc.append(PlanCarrera.objects.create(carrera=c[0],
                                             pub_date=date(2000, 1, 1),
                                             min_creditos=100,
                                             short_name='cocky_perlman00',
                                             orientacion='Namlrep Ykcoc'))
        pc.append(PlanCarrera.objects.create(carrera=c[1],
                                             pub_date=date(2000, 1, 1),
                                             min_creditos=100,
                                             short_name='berserk_hamil00'))
        pc.append(PlanCarrera.objects.create(carrera=c[2],
                                             pub_date=date(2000, 1, 1),
                                             min_creditos=100,
                                             short_name='angry_jang00'))
        a = []
        a.append(Alumno.objects.create(user=self.user, carrera=pc[0].carrera,
                                       plancarrera=pc[0],
                                       begin_date=date(2013, 1, 1)))
        a.append(Alumno.objects.create(user=self.user, carrera=pc[1].carrera,
                                       plancarrera=pc[1],
                                       begin_date=date(2013, 1, 1)))
        a.append(Alumno.objects.create(user=self.user, carrera=pc[2].carrera,
                                       plancarrera=pc[2],
                                       begin_date=date(2012, 1, 1)))

        d = Departamento.objects.create(codigo='95', name='Tests')
        m = Materia.objects.create(id='9501', departamento=d,
                                   codigo='01', name='sleepy_pani')
        pm = []
        pm.append(PlanMateria.objects.create(plancarrera=pc[0], materia=m,
                                             creditos=8, cuatrimestre='1'))
        AlumnoMateria.objects.create(user=self.user, materia=m, state='C')

class ViewsFacultadTestCase(BaseUserTestCase):

    def test_home(self):
        self.client.force_login(self.user)
        assert self.user.is_authenticated

        self.create_new_alumno()

        response = self.client.get(reverse('facultad:home'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Plan 2012')
        self.assertContains(response,
                            '<a href="/facultad/materias/cocky_perlman00/?' +
                            'show=todas" class="fiuba-minilogo"><span>cocky_' +
                            'perlman</span><br />')
        self.assertContains(response,
                            '<span class="small">Namlrep Ykcoc</span><br />')
        self.assertContains(response,
                            '<span class="small">Plan 2000</span></a></li>')
        self.assertContains(response,
                            '<a class="" href="/facultad/materia/9501/"')
        self.assertContains(response, '95.01')
        self.assertContains(response, 'sleepy_pani')

    def test_home_no_carrera(self):
        self.client.force_login(self.user)
        assert self.user.is_authenticated

        response = self.client.get(reverse('facultad:home'))
        self.assertEqual(response.status_code, 200)

        f = open('/tmp/x.html', 'wb')
        f.write(response.content)
        f.close()

        self.assertContains(response, '<span>No estás cursando ninguna materia.</span>')
        self.assertContains(response, '<a href="/facultad/carreras/add/">¿Qué carrera cursás?</a>')

    def test_plancarrera(self):
        self.client.force_login(self.user)
        assert self.user.is_authenticated

        self.create_new_alumno()

        response = self.client.get(reverse('facultad:materias-carrera',
                                           args=['cocky_perlman12']))
        self.assertEqual(response.status_code, 200)

    def test_get_correlativas(self):
        pass

    def test_materia(self):
        pass

    def test_menu_materias(self):
        pass

    def test_cargar_materias(self):
        pass
