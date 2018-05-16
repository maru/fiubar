from datetime import date

from ..models import Alumno, PlanMateria
from .common import BaseUserTestCase


class TestPlanMateriaManager(BaseUserTestCase):

    def test_list_materias_para_cursar_min_creditos_ok(self):
        pc = self.plan_carreras[0]
        m = self.materias[6]
        PlanMateria.objects.create(plancarrera=pc, materia=m,
                                   creditos=8, cuatrimestre='1',
                                   correlativas='4c')
        mat_list = PlanMateria.objects.list_materias_para_cursar(self.user, pc)
        self.assertEqual(mat_list.count(), 2)

    def test_list_materias_para_cursar_min_creditos_no(self):
        pc = self.plan_carreras[0]
        m = self.materias[6]
        PlanMateria.objects.create(plancarrera=pc, materia=m,
                                   creditos=8, cuatrimestre='1',
                                   correlativas='40c')
        mat_list = PlanMateria.objects.list_materias_para_cursar(self.user, pc)
        self.assertEqual(mat_list.count(), 1)

    def test_list_materias_para_cursar_min_creditos_bad(self):
        pc = self.plan_carreras[0]
        m = self.materias[6]
        PlanMateria.objects.create(plancarrera=pc, materia=m,
                                   creditos=8, cuatrimestre='1',
                                   correlativas='c')
        mat_list = PlanMateria.objects.list_materias_para_cursar(self.user, pc)
        self.assertEqual(mat_list.count(), 2)

    def test_list_materias_cursando_empty(self):
        pc = self.plan_carreras[1]
        Alumno.objects.create(user=self.user, carrera=pc.carrera,
                              plancarrera=pc, begin_date=date(2017, 1, 10))

        mat_list = PlanMateria.objects.list_materias_cursando(self.user, pc)
        self.assertEqual(mat_list.count(), 0)

    def test_list_materias_cursando_1_materia(self):
        pc = self.plan_carreras[0]
        mat_list = PlanMateria.objects.list_materias_cursando(self.user, pc)
        self.assertEqual(mat_list.count(), 1)

    def test_list_materias_para_cursar_no_alumno(self):
        pc = self.plan_carreras[3]
        mat_list = PlanMateria.objects.list_materias_para_cursar(self.user, pc)
        self.assertEqual(mat_list, [])
