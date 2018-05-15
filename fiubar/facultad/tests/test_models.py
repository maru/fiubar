from datetime import date

from django.urls import reverse

from ..models import (AlumnoMateria, Carrera, Correlativa, Departamento,
                      Materia, PlanCarrera, PlanMateria)
from .common import BaseUserTestCase


class TestAlumnoModel(BaseUserTestCase):

    def test_str(self):
        pc = self.plan_carreras[0]
        a = self.alumnos[0]
        self.assertEqual(str(a), '%s/%s' % (self.user, pc))

    def test_url_delete(self):
        a = self.alumnos[0]
        pc = self.plan_carreras[0]
        self.assertEqual(
            reverse('facultad:carreras-delete',
                    kwargs={'plancarrera': pc.short_name}),
            a.url_delete()
        )

    def test_url_materias(self):
        pc = self.plan_carreras[0]
        a = self.alumnos[0]
        self.assertEqual(
            reverse('facultad:materias-carrera',
                    kwargs={'plancarrera': pc.short_name}),
            a.url_materias()
        )

    def test_url_materias_tab_todas(self):
        pc = self.plan_carreras[0]
        a = self.alumnos[0]
        self.assertEqual(
            reverse('facultad:materias-carrera',
                    kwargs={'plancarrera':
                            pc.short_name}) + '?show=todas',
            a.url_materias_tab_todas()
        )

    def test_url_graduado(self):
        pc = self.plan_carreras[0]
        a = self.alumnos[0]
        self.assertEqual(
            reverse('facultad:carreras-graduado',
                    kwargs={'plancarrera': pc.short_name}),
            a.url_graduado()
        )

    def test_url_del_graduado(self):
        pc = self.plan_carreras[0]
        a = self.alumnos[0]
        self.assertEqual(
            reverse('facultad:carreras-graduado-delete',
                    kwargs={'plancarrera': pc.short_name}),
            a.url_del_graduado()
        )

    def test_get_creditos(self):
        a = self.alumnos[0]
        pc = a.plancarrera
        aprobadas = [m.materia for m in AlumnoMateria.objects.filter
                     (user=a.user).exclude(state__in=['C', 'F'])]
        materias = PlanMateria.objects.filter(plancarrera=pc,
                                              materia__in=aprobadas)
        creditos = [pm.creditos for pm in materias]
        creditos = sum(creditos) * 100 / pc.min_creditos
        self.assertEqual(creditos, a.get_creditos())

    def test_del_graduado(self):
        a = self.alumnos[0]
        a.graduado_date = date(2020, 2, 20)
        a.del_graduado()
        self.assertIsNone(a.graduado_date)

    def test_is_graduado(self):
        a = self.alumnos[0]
        self.assertIsNone(a.graduado_date)
        a.graduado_date = date(2020, 2, 20)
        self.assertIsNotNone(a.is_graduado())

    def test_tiempo_carrera(self):
        a = self.alumnos[0]
        a.graduado_date = date(2020, 2, 20)
        self.assertEqual(a.tiempo_carrera(), '7 años')


class TestAlumnoMateriaModel(BaseUserTestCase):

    def test_str(self):
        m = Materia(id='9501')
        am = AlumnoMateria(user=self.user, materia=m)
        self.assertEqual(str(am), '%s/%s' % (self.user, m))


class TestCarreraModel(BaseUserTestCase):

    def test_str(self):
        c = Carrera(short_name='nueva_carrera')
        self.assertEqual(str(c), c.short_name)


class TestPlanCarreraModel(BaseUserTestCase):

    def test_str(self):
        pc = PlanCarrera(name='Nuevo Plan Carrera')
        self.assertEqual(str(pc), pc.name)


class TestDepartamentoModel(BaseUserTestCase):

    def test_str(self):
        d = Departamento(codigo='95')
        self.assertEqual(str(d), d.codigo)


class TestMateriaModel(BaseUserTestCase):

    def test_str(self):
        m = Materia(id='9501')
        self.assertEqual(str(m), m.id)


class TestPlanMateriaModel(BaseUserTestCase):

    def test_str(self):
        pc = PlanCarrera(name='Nuevo Plan Carrera')
        m = Materia(id='9501')
        pm = PlanMateria(plancarrera=pc, materia=m)
        self.assertEqual(str(pm), '%s/%s' % (pm.plancarrera, pm.materia))


class TestCorrelativaModel(BaseUserTestCase):

    def test_str(self):
        pc = PlanCarrera(name='Nuevo Plan Carrera')
        m1 = Materia(id='9501')
        m2 = Materia(id='9502')
        pm1 = PlanMateria(plancarrera=pc, materia=m1)
        pm2 = PlanMateria(plancarrera=pc, materia=m2)
        c = Correlativa(materia=pm1, correlativa=pm2)
        self.assertEqual(str(c), str(c.materia))
