# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.db import models


Q = models.Q


class AlumnoManager(models.Manager):
    def create(self, **kwargs):
        list = self.filter(user=kwargs['user'], carrera=kwargs['carrera'],
                           plancarrera=kwargs['plancarrera'])
        if list.count() > 0:
            return None
        alumno = super(AlumnoManager, self).create(**kwargs)
        return alumno

    def get_summary(self, user):
        return []
        list_carreras = self.select_related().filter(user=user)
        for a in list_carreras:
            a.new_alumnos = self.filter(carrera=a.carrera).count()
        return list_carreras

    def count_new(self, user, begin_date=None):
        """Counts new alumnos in carreras cursadas by user"""
        car_list = self.filter(user=user)
        new_list = []
        for a in car_list:
            alist = self.filter(carrera=a.carrera).exclude(user=user)
            if begin_date:
                alist = alist.filter(creation_date__gte=begin_date)
            a.new_alumnos = alist.count()
            if a.new_alumnos:
                new_list.append(a)
        return new_list


class AlumnoMateriaManager(models.Manager):

    def get_initial_data(self, user, materia):
        d = {}
        try:
            am = self.get(user=user, materia=materia)
            d['nota'] = am.nota
            d['state'] = am.state
            d['cursada_date'] = am.cursada_date
            d['aprobada_date'] = am.aprobada_date
            if am.cursada_cuat:
                d['cursada_cuat'], d['cursada_year'] = \
                    am.cursada_cuat.split('-')
            if am.aprobada_cuat:
                d['aprobada_cuat'], d['aprobada_year'] = \
                    am.aprobada_cuat.split('-')
        except ObjectDoesNotExist:
            pass
        return d

    def list_materias(self, user):
        return self.filter(user=user)

    def list_materias_cursando(self, user):
        return self.list_materias(user=user)\
            .filter(Q(state='C') | Q(state='F'))

    def list_materias_aprobadas(self, user):
        return self.list_materias(user=user)\
            .filter(Q(state='A') | Q(state='E'))\
            .order_by('aprobada_date', 'materia')

    def get_summary(self, user):
        list_matcur = self.list_materias_cursando(user).order_by('state')
        for m in list_matcur:
            m.new_alumnos = self.filter(materia=m.materia).count()
        return list_matcur

    def count_new(self, user, begin_date):
        """Counts new alumnos in materias cursadas by user"""
        mat_list = self.list_materias_cursando(user).order_by('state')
        new_list = []
        for m in mat_list:
            mlist = self.filter(materia=m.materia).exclude(user=user)
            if begin_date:
                mlist = mlist.filter(creation_date__gte=begin_date)
            m.new_alumnos = mlist.count()
            if m.new_alumnos:
                new_list.append(m)
        return new_list

    def create_or_update(self, user, materia, final_date, nota):
        try:
            al = self.get(user=user, materia=materia)
            al.state = 'A'
            al.aprobada_date = final_date
            al.nota = nota
        except ObjectDoesNotExist:
            al = self.create(user=user, materia=materia, state='A',
                             aprobada_date=final_date, nota=nota)
        al.aprobada_date_to_cuat()
        al.save()
        return al

    def get_or_none(self, user, materia):
        try:
            materia_cursada = self.get(user=user, materia=materia)
        except ObjectDoesNotExist:
            materia_cursada = None
        return materia_cursada

    def update_creditos(self, user, list_carreras):
        from .models import PlanMateria
        materias_cursadas = self.filter(user=user)
        # Recalculo los créditos para cada carrera
        for al in list_carreras:
            al.creditos = 0
            al.promedio = 0.0
            count_materias = 0
            for m in materias_cursadas:
                if not (m.aprobada() or m.equivalencia()):
                    continue
                # Check si materia existe en carrera
                materia = PlanMateria.objects\
                    .filter(plancarrera=al.plancarrera, materia=m.materia)
                # Update de creditos en carrera
                if materia.count():
                    al.creditos += materia[0].creditos
                    if m.nota > 0:
                        al.promedio += m.nota
                        count_materias += 1
            if count_materias:
                al.promedio = round(al.promedio / count_materias, 2)
            al.save()
        return


class PlanMateriaManager(models.Manager):

    def list_materias_para_cursar(self, user, plancarrera):
        from .models import Alumno, AlumnoMateria, Correlativa
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
        from .models import AlumnoMateria

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
        from .models import AlumnoMateria

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
        from .models import AlumnoMateria

        am_list = AlumnoMateria.objects.list_materias(user)
        list = self.filter(plancarrera=plancarrera)
        for am in am_list:
            list = list.exclude(materia=am.materia)
        list = list.order_by('cuatrimestre')
        return list
