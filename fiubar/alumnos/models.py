# -*- coding: utf-8 -*-
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext as _

from .managers import MateriaManager, PlanCarreraManager
from .utils import calculate_time

from fiubar.facultad.models import Carrera
from fiubar.facultad.models import Materia as FacultadMateria
from fiubar.facultad.models import PlanCarrera as FacultadPlanCarrera
from fiubar.users.models import User


class PlanCarrera(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE,
                                related_name='+', null=True)
    plancarrera = models.ForeignKey(FacultadPlanCarrera,
                                    on_delete=models.CASCADE, null=True)
    begin_date = models.DateField()
    graduado_date = models.DateField(null=True)
    creditos = models.IntegerField(default=0)
    promedio = models.FloatField(default=0.0)
    creation_date = models.DateTimeField(auto_now_add=True)

    objects = PlanCarreraManager()

    def __str__(self):
        return self.user

    def url_delete(self):
        return reverse('facultad:carreras-delete',
                       args=[self.plancarrera.short_name])

    def url_materias(self):
        return reverse('facultad:materias-carrera',
                       args=[self.plancarrera.short_name])

    def url_materias_tab_todas(self):
        return reverse('facultad:materias-carrera',
                       args=[self.plancarrera.short_name]) + '?show=todas'

    def url_graduado(self):
        return reverse('facultad:carreras-graduado',
                       args=[self.plancarrera.short_name])

    def url_del_graduado(self):
        return reverse('facultad:carrera-graduado-del',
                       args=[self.plancarrera.short_name])

    def url_profile(self):
        return self.user.profile_set.all()[0].url_profile()

    def get_creditos(self):
        return (self.creditos * 100 / self.plancarrera.min_creditos)

    def del_graduado(self):
        self.graduado_date = None
        self.save()

    def is_graduado(self):
        return self.graduado_date

    def tiempo_carrera(self):
        return calculate_time(self.begin_date, self.graduado_date)

    def begin_date_to_cuat(self):
        if not self.begin_date:
            return ''
        to_cuatrimestre = {2: 'V', 3: '1', 8: '2'}
        cuatrimestre = to_cuatrimestre[self.begin_date.month]
        return _('%(cuatrimestre)s° Cuatrimestre %(year)s') % \
                ({'cuatrimestre': cuatrimestre,
                  'year': self.begin_date.year})

    class Meta:
        unique_together = (('user', 'plancarrera'),)


class Materia(models.Model):
    CUATRIMESTRES = (
        ('1', '1'),
        ('2', '2'),
        ('V', _('Verano')),
    )

    MATERIA_STATE = (
        ('C', _('Cursando')),
        ('F', _('Cursada Aprobada')),
        ('A', _('Materia Aprobada')),
        ('E', _('Equivalencia')),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    materia = models.ForeignKey(FacultadMateria, on_delete=models.CASCADE,
                                null=True)
    state = models.CharField(choices=MATERIA_STATE, default='C', max_length=1)
    cursada_cuat = models.CharField(max_length=10, null=True, blank=True)
    cursada_date = models.DateField(null=True, blank=True)
    aprobada_cuat = models.CharField(max_length=10, null=True, blank=True)
    aprobada_date = models.DateField(null=True, blank=True)
    nota = models.IntegerField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    objects = MateriaManager()

    def __str__(self):
        return '%s' % (self.materia)

    def update(self, user, materia, d):
        self.user = user
        self.materia = materia
        self.state = d.get('state', 'C')
        self.nota = d.get('nota', 0)

        # Fecha de cursada
        cursada_cuat = d.get('cursada_cuat')
        cursada_year = d.get('cursada_year')
        self.cursada_cuat = None
        self.cursada_date = d.get('cursada_date')
        if cursada_cuat and cursada_year:
            self.cursada_cuat = '%s-%s' % (cursada_cuat, cursada_year)
            if not self.cursada_date:
                self.cursada_cuat_to_date(cursada_cuat, cursada_year)

        # Fecha de aprobada
        aprobada_cuat = d.get('aprobada_cuat')
        aprobada_year = d.get('aprobada_year')
        self.aprobada_cuat = None
        self.aprobada_date = d.get('aprobada_date')
        if aprobada_cuat and aprobada_year:
            self.aprobada_cuat = '%s-%s' % (aprobada_cuat, aprobada_year)
            if not self.aprobada_date:
                self.aprobada_cuat_to_date(aprobada_cuat, aprobada_year)

    def get_aprobada_cuat(self):
        if not self.aprobada_cuat and not self.aprobada_date:
            return '-'
        if not self.aprobada_cuat:
            self.aprobada_date_to_cuat()
        cuatrimestre, year = self.aprobada_cuat.split('-')
        if cuatrimestre == 'V':
            return _('Verano %(year)s') % ({'year': year})
        return _('%(cuatrimestre)s° Cuatrimestre %(year)s') % \
                ({'cuatrimestre': cuatrimestre, 'year': year})

    def cursando(self):
        return (self.state == 'C')

    def falta_final(self):
        return (self.state == 'F')

    def aprobada(self):
        return (self.state == 'A')

    def equivalencia(self):
        return (self.state == 'E')

    def aprobada_cuat_to_date(self, cuat, year):
        dict_aprobada_cuat = {'V': 2, '1': 7, '2': 12}
        import datetime
        d = datetime.date(int(year), dict_aprobada_cuat.get(cuat, 1), 1)
        self.aprobada_date = d

    def aprobada_date_to_cuat(self):
        dict_aprobada_month = {6: '1', 7: '1', 8: '1', 9: '1', 10: '1',
                               1: '2', 2: '2', 3: '2', 4: '2', 5: '2',
                               11: '2', 12: '2'}
        cuatrimestre = dict_aprobada_month.get(self.aprobada_date.month, None)
        year = self.aprobada_date.year
        if self.aprobada_date.month < 6:
            year -= 1
        self.aprobada_cuat = '%s-%s' % (cuatrimestre, year)

    def cursada_cuat_to_date(self, cuat, year):
        dict_cursada_cuat = {'V': 2, '1': 3, '2': 8}
        import datetime
        d = datetime.date(int(year), dict_cursada_cuat.get(cuat, 1), 1)
        self.cursada_date = d

    def cursada_date_to_cuat(self):
        dict_cursada_month = {2: 'V', 3: '1', 8: '2'}
        cuatrimestre = dict_cursada_month.get(self.cursada_date.month, 0)
        self.cursada_cuat = '%s-%s' % (cuatrimestre, self.cursada_date.year)

    class Meta:
        unique_together = (('user', 'materia'),)
