# -*- coding: utf-8 -*-
from django.db import models


Q = models.Q


class PlanCarreraManager(models.Manager):
    def create(self, **kwargs):
        list = self.filter(user=kwargs['user'], carrera=kwargs['carrera'],
                           plancarrera=kwargs['plancarrera'])
        if list.count() > 0:
            return None
        alumno = super(PlanCarreraManager, self).create(**kwargs)
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


class MateriaManager(models.Manager):

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
        except self.model.DoesNotExist:
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
        except self.model.DoesNotExist:
            al = self.create(user=user, materia=materia, state='A',
                             aprobada_date=final_date, nota=nota)
        al.aprobada_date_to_cuat()
        al.save()
        return al

    def get_or_none(self, user, materia):
        try:
            materia_cursada = self.get(user=user, materia=materia)
        except self.model.DoesNotExist:
            materia_cursada = None
        return materia_cursada

    def update_creditos(self, user, list_carreras):
        from fiubar.facultad.models import PlanMateria
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
