# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.db import models


Q = models.Q


class AlumnoManager(models.Manager):
    def create(self, **kwargs):
        pc = kwargs['plancarrera']
        al_list = self.filter(user=kwargs['user'], carrera=pc.carrera,
                              plancarrera=pc)
        if al_list.count() > 0:
            return None
        alumno = super(AlumnoManager, self).create(**kwargs)
        return alumno


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

    def update_creditos(self, user, list_carreras=None):
        from .models import Alumno, PlanMateria
        materias_cursadas = self.filter(user=user)
        if list_carreras is None:
            list_carreras = Alumno.objects.select_related('carrera')\
                .filter(user=user).order_by('plancarrera')
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

        # Verificar que user es alumno del plancarrera
        try:
            alumno = Alumno.objects.get(user=user, plancarrera=plancarrera)
        except ObjectDoesNotExist:
            return []

        # Materias cursadas y aprobadas
        am_list = AlumnoMateria.objects.filter(user=user)
        cursada_list = [am.materia for am in am_list]

        # PlanMaterias del plancarrera
        pm_list = self.filter(plancarrera=plancarrera)\
            .exclude(materia__in=cursada_list).order_by('cuatrimestre')

        aprobada_list = [am.materia
                         for am in am_list.filter(state__in=['A', 'E'])]

        # Filtrar materias con correlativas no aprobadas
        co_list = Correlativa.objects.filter(materia__plancarrera=plancarrera)
        co_list = co_list.exclude(correlativa__materia__in=aprobada_list)\
            .exclude(correlativa=None)
        co_list = [c.materia.materia for c in co_list]

        pm_list = pm_list.exclude(materia__in=co_list)

        for pm in pm_list:
            try:
                if pm.correlativas[-1] != 'c':
                    continue
                mat_cred = int(pm.correlativas.strip('c'))
                if alumno.creditos < mat_cred:
                    pm_list = pm_list.exclude(pk=pm.pk)
            except (ValueError, AttributeError) as e:
                import logging
                logger = logging.getLogger('fiubar')
                logger.error('PlanMateriaManager.list_materias_para_cursar: '
                             '%s - %s' % (pm, e))
        return pm_list

    def list_materias_cursando(self, user, plancarrera):
        from .models import AlumnoMateria

        aprobada_list = AlumnoMateria.objects.list_materias_cursando(user)

        mat_list = None
        for m in aprobada_list:
            if not mat_list:
                mat_list = Q(plancarrera=plancarrera, materia=m.materia)
            else:
                mat_list |= Q(plancarrera=plancarrera, materia=m.materia)
        return self.filter(mat_list).order_by('cuatrimestre')

    def list_materias_aprobadas(self, user, plancarrera):
        from .models import AlumnoMateria

        aprobada_list = AlumnoMateria.objects.list_materias_aprobadas(user)

        mat_list = None
        for m in aprobada_list:
            if not mat_list:
                mat_list = Q(plancarrera=plancarrera, materia=m.materia)
            else:
                mat_list = mat_list | Q(plancarrera=plancarrera,
                                        materia=m.materia)
        if mat_list:
            mat_list = self.filter(mat_list).order_by('cuatrimestre')
            for m in mat_list:
                mat = aprobada_list.get(materia=m.materia)
                m.state = mat.state
                m.aprobada_cuat = mat.aprobada_cuat
                m.aprobada_date = mat.aprobada_date
        return mat_list
