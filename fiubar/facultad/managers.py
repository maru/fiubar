# -*- coding: utf-8 -*-
from django.db import models


Q = models.Q


class PlanMateriaManager(models.Manager):

    def list_materias_para_cursar(self, user, plancarrera):
        from fiubar.alumnos.models import PlanCarrera as Alumno
        from fiubar.alumnos.models import Materia as AlumnoMateria
        from .models import Correlativa
        # Materias cursadas y aprobadas
        am_list = AlumnoMateria.objects.list_materias(user)
        aprobada_list = AlumnoMateria.objects.list_materias_aprobadas(user)

        # Lista de todas las correlativas
        co_list = Correlativa.objects.filter(materia__plancarrera=plancarrera)

        # Saco las que tienen las correlativas aprobadas
        Qap = None
        if aprobada_list.count() > 0:
            for m in aprobada_list:
                if not Qap:
                    Qap = Q(correlativa__materia=m.materia)
                else:
                    Qap = Qap | Q(correlativa__materia=m.materia)
        if Qap:
            co_list = co_list.exclude(Qap)

        Qcur = None
        if am_list.count() > 0:
            for m in am_list:
                if not Qcur:
                    Qcur = Q(materia=m.materia)
                else:
                    Qcur = Qcur | Q(materia=m.materia)

        Qcor = None
        for m in co_list:
            if not Qcor:
                Qcor = Q(id=m.materia.id)
            else:
                Qcor = Qcor | Q(id=m.materia.id)

        # En co_list saco las que tienen alguna correlativa aprobada.
        list = self.filter(plancarrera=plancarrera)

        # Saco las que ya estoy cursando o aprobe
        if Qcur:
            list = list.exclude(Qcur)

        # Saco las que tienen correlativas por hacer...
        if Qcor:
            list = list.exclude(Qcor)

        # Saco las que tienen un minimo de creditos
        a = Alumno.objects.get(user=user, plancarrera=plancarrera)

        l_cred = list.order_by('cuatrimestre')
        list = []
        for e in l_cred:
            try:
                mat_cred = int(e.correlativas.strip('c'))
                if a.creditos >= mat_cred:
                    list.append(e)
            except ValueError:
                list.append(e)
        return list

    def list_materias_cursando(self, user, plancarrera):
        from fiubar.alumnos.models import Materia as AlumnoMateria

        aprobada_list = AlumnoMateria.objects.list_materias_cursando(user)

        list = None
        for m in aprobada_list:
            if not list:
                list = Q(plancarrera=plancarrera, materia=m.materia)
            else:
                list = list | Q(plancarrera=plancarrera, materia=m.materia)
        if list:
            return self.filter(list).order_by('cuatrimestre')
        return None

    def list_materias_aprobadas(self, user, plancarrera):
        from fiubar.alumnos.models import Materia as AlumnoMateria

        aprobada_list = AlumnoMateria.objects.list_materias_aprobadas(user)

        list = None
        for m in aprobada_list:
            if not list:
                list = Q(plancarrera=plancarrera, materia=m.materia)
            else:
                list = list | Q(plancarrera=plancarrera, materia=m.materia)
        if list:
            list = self.filter(list).order_by('cuatrimestre')
            for m in list:
                mat = aprobada_list.get(materia=m.materia)
                m.state = mat.state
                m.aprobada_cuat = mat.aprobada_cuat
                m.aprobada_date = mat.aprobada_date
        return list

    def list_materias_faltan_correl(self, user, plancarrera):
        from fiubar.alumnos.models import Materia as AlumnoMateria

        am_list = AlumnoMateria.objects.list_materias(user)
        list = self.filter(plancarrera=plancarrera)
        for am in am_list:
            list = list.exclude(materia=am.materia)
        list = list.order_by('cuatrimestre')
        return list
