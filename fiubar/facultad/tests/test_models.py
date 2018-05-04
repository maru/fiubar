from django.urls import reverse
from test_plus.test import TestCase

from ..models import (Alumno, AlumnoMateria, Carrera, Correlativa, Departamento, Materia, PlanCarrera,
                      PlanMateria)


class BaseTestCase(TestCase):
    def setUp(self):
        self.user = self.make_user()


class TestAlumnoModel(BaseTestCase):

    def create_new_alumno(self):
        self.c = Carrera(codigo='codg', name='Nueva Carrera',
                         abbr_name='Nva. Carr.',
                         short_name='nueva_carrera')
        self.c.save()

        self.pc = PlanCarrera(short_name='nuevo_plan_carrera',
                              name='Nuevo Plan Carrera',
                              min_creditos=100,
                              carrera=self.c,
                              pub_date='2012-12-12')
        self.pc.save()

        d = Departamento(codigo='95', name='Tests')
        d.save()
        
        m = Materia(id='95.01', departamento=d,
                    codigo='01', name='new_materia')
        m.save()

        self.pm = PlanMateria(plancarrera=self.pc,
                              materia=m,
                              creditos=8,
                              cuatrimestre='1')
        self.pm.save()

        self.a = Alumno(user=self.user,
                        carrera=self.c,
                        plancarrera=self.pc,
                        begin_date='2013-01-10')
        self.a.save()

        am = AlumnoMateria(user=self.user,
                           materia=m,
                           state='A')
        am.save()

        AlumnoMateria.objects.update_creditos(self.user, [self.a])

    def test_str(self):
        self.create_new_alumno()
        self.assertEqual(str(self.a), '%s/%s' % (self.user, self.pc))

    def test_url_delete(self):
        self.create_new_alumno()
        self.assertEqual(
            reverse('facultad:carreras-delete',
                    kwargs={'plancarrera': self.pc.short_name}),
            self.a.url_delete()
        )

    def test_url_materias(self):
        self.create_new_alumno()
        self.assertEqual(
            reverse('facultad:materias-carrera',
                    kwargs={'plancarrera': self.pc.short_name}),
            self.a.url_materias()
        )

    def test_url_materias_tab_todas(self):
        self.create_new_alumno()
        self.assertEqual(
            reverse('facultad:materias-carrera',
                    kwargs={'plancarrera': self.pc.short_name}) + '?show=todas',
            self.a.url_materias_tab_todas()
        )

    def test_url_graduado(self):
        self.create_new_alumno()
        self.assertEqual(
            reverse('facultad:carreras-graduado',
                    kwargs={'plancarrera' : self.pc.short_name}),
            self.a.url_graduado()
        )

    def test_url_del_graduado(self):
        self.create_new_alumno()
        self.assertEqual(
            reverse('facultad:carrera-graduado-del',
                    kwargs={'plancarrera' : self.pc.short_name}),
            self.a.url_del_graduado()
        )

    def test_get_creditos(self):
        self.create_new_alumno()
        creditos = self.pm.creditos * 100 / self.pc.min_creditos
        self.assertEqual(creditos, self.a.get_creditos())

    def test_url_materias(self):
        self.create_new_alumno()
        self.assertEqual(
            reverse('facultad:materias-carrera',
                    kwargs={'plancarrera' : self.pc.short_name}),
            self.a.url_materias()
        )

    def test_url_materias(self):
        self.create_new_alumno()
        self.assertEqual(
            reverse('facultad:materias-carrera',
                    kwargs={'plancarrera' : self.pc.short_name}),
            self.a.url_materias()
        )

    def test_url_materias(self):
        self.create_new_alumno()
        self.assertEqual(
            reverse('facultad:materias-carrera',
                    kwargs={'plancarrera' : self.pc.short_name}),
            self.a.url_materias()
        )


class TestAlumnoMateriaModel(BaseTestCase):

    def test_str(self):
        m = Materia(id='95.01')
        am = AlumnoMateria(user=self.user,materia=m)
        self.assertEqual(str(am), '%s/%s' % (self.user, m))


class TestCarreraModel(BaseTestCase):

    def test_str(self):
        c = Carrera(short_name='nueva_carrera')
        self.assertEqual(str(c), c.short_name)


class TestPlanCarreraModel(BaseTestCase):

    def test_str(self):
        pc = PlanCarrera(name='Nuevo Plan Carrera')
        self.assertEqual(str(pc), pc.name)


class TestDepartamentoModel(BaseTestCase):

    def test_str(self):
        d = Departamento(codigo='95')
        self.assertEqual(str(d), d.codigo)


class TestMateriaModel(BaseTestCase):

    def test_str(self):
        m = Materia(id='95.01')
        self.assertEqual(str(m), m.id)


class TestPlanMateriaModel(BaseTestCase):

    def test_str(self):
        pc = PlanCarrera(name='Nuevo Plan Carrera')
        m = Materia(id='95.01')
        pm = PlanMateria(plancarrera=pc, materia=m)
        self.assertEqual(str(pm), '%s/%s' % (pm.plancarrera, pm.materia))


class TestCorrelativaModel(BaseTestCase):

    def test_str(self):
        pc = PlanCarrera(name='Nuevo Plan Carrera')
        m1 = Materia(id='95.01')
        m2 = Materia(id='95.02')
        pm1 = PlanMateria(plancarrera=pc, materia=m1)
        pm2 = PlanMateria(plancarrera=pc, materia=m2)
        c = Correlativa(materia=pm1, correlativa=pm2)
        self.assertEqual(str(c), str(c.materia))
