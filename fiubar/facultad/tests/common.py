from datetime import date

from test_plus.test import TestCase

from ..models import (Alumno, AlumnoMateria, Carrera, Correlativa,
                      Departamento, Materia, PlanCarrera, PlanMateria)


class BaseTestCase(TestCase):

    def setUp(self):
        self.create_new_facultad()

    def create_new_facultad(self):
        c = []
        c.append(Carrera.objects.create(codigo='a', abbr_name='cocky_perlman'))
        c.append(Carrera.objects.create(codigo='b', abbr_name='berserk_hamil'))
        c.append(Carrera.objects.create(codigo='c', abbr_name='angry_jang'))
        c.append(Carrera.objects.create(codigo='codg', name='Nueva Carrera',
                                        abbr_name='Nva. Carr.',
                                        short_name='nueva_carrera'))
        self.carreras = c

        pc = []
        pc.append(PlanCarrera.objects.create(carrera=c[0],
                                             pub_date=date(2012, 1, 1),
                                             min_creditos=100,
                                             name='Cocky Perlman 2012',
                                             short_name='cocky_perlman12'))
        pc.append(PlanCarrera.objects.create(carrera=c[0],
                                             pub_date=date(2000, 1, 1),
                                             min_creditos=100,
                                             name='Cocky Perlman 2000',
                                             short_name='cocky_perlman00',
                                             orientacion='Namlrep Ykcoc'))
        pc.append(PlanCarrera.objects.create(carrera=c[1],
                                             pub_date=date(2000, 1, 1),
                                             min_creditos=100,
                                             name='Berserk Hamil 2000',
                                             short_name='berserk_hamil00'))
        pc.append(PlanCarrera.objects.create(carrera=c[2],
                                             pub_date=date(2000, 1, 1),
                                             min_creditos=100,
                                             name='Angry Jang 2000',
                                             short_name='angry_jang00'))
        pc.append(PlanCarrera.objects.create(short_name='nuevo_plan_carrera',
                                             name='Nuevo Plan Carrera',
                                             min_creditos=100,
                                             carrera=c[3],
                                             pub_date=date(2012, 12, 12)))
        self.plan_carreras = pc

        d = []
        d.append(Departamento.objects.create(codigo='95', name='Tests'))
        d.append(Departamento.objects.create(codigo='61', name='Matematica'))
        d.append(Departamento.objects.create(codigo='62', name='Fisica'))
        self.departamentos = d

        m = []
        m.append(Materia.objects.create(id='9501', departamento=d[0],
                                        codigo='01', name='sleepy_pani'))
        m.append(Materia.objects.create(id='9502', departamento=d[0],
                                        codigo='02', name='nostalgic_bell'))
        m.append(Materia.objects.create(id='9503', departamento=d[0],
                                        codigo='03', name='loving_perlman'))
        m.append(Materia.objects.create(id='6108', departamento=d[1],
                                        codigo='08',
                                        name='Analisis Matematico II'))
        m.append(Materia.objects.create(id='6103', departamento=d[1],
                                        codigo='03', name='Algebra II'))
        m.append(Materia.objects.create(id='6109', departamento=d[1],
                                        codigo='09', name='Probabilidad'))
        m.append(Materia.objects.create(id='6202', departamento=d[2],
                                        codigo='02', name='Fisica II'))
        m.append(Materia.objects.create(id='6205', departamento=d[2],
                                        codigo='05', name='Fisica V'))
        self.materias = m

        pm = []
        pm.append(PlanMateria.objects.create(plancarrera=pc[0], materia=m[0],
                                             creditos=8, cuatrimestre='1',
                                             correlativas=''))
        pm.append(PlanMateria.objects.create(plancarrera=pc[0], materia=m[1],
                                             creditos=4, cuatrimestre='2',
                                             correlativas='9501'))
        pm.append(PlanMateria.objects.create(plancarrera=pc[4], materia=m[2],
                                             creditos=6, cuatrimestre='3',
                                             correlativas='9502'))
        pm.append(PlanMateria.objects.create(plancarrera=pc[4], materia=m[3],
                                             creditos=8, cuatrimestre='1',
                                             correlativas='CBC'))
        pm.append(PlanMateria.objects.create(plancarrera=pc[4], materia=m[4],
                                             creditos=8, cuatrimestre='1',
                                             correlativas='CBC'))
        pm.append(PlanMateria.objects.create(plancarrera=pc[4], materia=m[5],
                                             creditos=8, cuatrimestre='2',
                                             correlativas='61.03-61.08'))
        pm.append(PlanMateria.objects.create(plancarrera=pc[4], materia=m[6],
                                             creditos=6, cuatrimestre='1',
                                             correlativas='61.08'))
        pm.append(PlanMateria.objects.create(plancarrera=pc[3], materia=m[7],
                                             creditos=6, cuatrimestre='2',
                                             correlativas='62.02'))
        self.plan_materias = pm

        Correlativa.objects.create(materia=pm[1], correlativa=pm[0])
        Correlativa.objects.create(materia=pm[2], correlativa=pm[1])
        Correlativa.objects.create(materia=pm[5], correlativa=pm[3])
        Correlativa.objects.create(materia=pm[5], correlativa=pm[4])
        Correlativa.objects.create(materia=pm[6], correlativa=pm[3])
        Correlativa.objects.create(materia=pm[7], correlativa=pm[6])


class BaseUserTestCase(BaseTestCase):

    def setUp(self):
        super(BaseUserTestCase, self).setUp()

        self.user = self.make_user()

        self.client.force_login(self.user)
        assert self.user.is_authenticated

        self.create_new_alumno()

    def create_new_alumno(self):
        a = []
        pc = self.plan_carreras[0]
        a.append(Alumno.objects.create(user=self.user, carrera=pc.carrera,
                                       plancarrera=pc,
                                       begin_date=date(2013, 1, 1)))
        pc = self.plan_carreras[1]
        a.append(Alumno.objects.create(user=self.user, carrera=pc.carrera,
                                       plancarrera=pc,
                                       begin_date=date(2013, 1, 1)))
        pc = self.plan_carreras[2]
        a.append(Alumno.objects.create(user=self.user, carrera=pc.carrera,
                                       plancarrera=pc,
                                       begin_date=date(2012, 1, 1)))
        pc = self.plan_carreras[4]
        a.append(Alumno.objects.create(user=self.user, carrera=pc.carrera,
                                       plancarrera=pc,
                                       begin_date=date(2013, 1, 10)))

        self.user2 = self.make_user('user_2')
        pc = self.plan_carreras[3]
        a.append(Alumno.objects.create(user=self.user2, carrera=pc.carrera,
                                       plancarrera=pc,
                                       begin_date=date(2017, 1, 10)))
        self.alumnos = a

        am = []
        am.append(AlumnoMateria.objects.create(user=self.user,
                                               materia=self.materias[2],
                                               state='C'))
        am.append(AlumnoMateria.objects.create(user=self.user,
                                               materia=self.materias[1],
                                               state='F'))
        am.append(AlumnoMateria.objects.create(user=self.user,
                                               materia=self.materias[0],
                                               state='A', nota=7))
        am.append(AlumnoMateria.objects.create(user=self.user,
                                               materia=self.materias[3],
                                               state='E'))
        self.alumno_materia = am

        AlumnoMateria.objects.update_creditos(self.user, self.alumnos)
