# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext as _

from .managers import AlumnoManager, AlumnoMateriaManager, PlanMateriaManager

from fiubar.users.models import User


class Alumno(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    carrera = models.ForeignKey('Carrera', on_delete=models.CASCADE)
    plancarrera = models.ForeignKey('PlanCarrera', on_delete=models.CASCADE)
    begin_date = models.DateField()
    graduado_date = models.DateField(null=True)
    creditos = models.IntegerField(default=0)
    promedio = models.FloatField(default=0.0)
    creation_date = models.DateTimeField(auto_now_add=True)

    objects = AlumnoManager()

    def __str__(self):
        return '%s/%s' % (self.user, self.plancarrera)

    def save(self, *args, **kwargs):
        self.clean()
        return super(Alumno, self).save(*args, **kwargs)

    def clean(self):
        """
        Validar que la fecha graduado_date sea mayor que la fecha begin_date.
        """
        if (self.graduado_date is None) or (self.begin_date is None):
            return

        if int(self.graduado_date.toordinal()) \
           <= int(self.begin_date.toordinal()):
            raise ValidationError(
                _('%(graduado_date)s es anterior a la fecha de comienzo '
                  '%(begin_date)s'),
                params={'graduado_date': self.graduado_date,
                        'begin_date': self.begin_date},
            )

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
        return reverse('facultad:carreras-graduado-delete',
                       args=[self.plancarrera.short_name])

    def get_creditos(self):
        return (self.creditos * 100 / self.plancarrera.min_creditos)

    def del_graduado(self):
        self.graduado_date = None
        self.save()

    def is_graduado(self):
        return self.graduado_date

    def tiempo_carrera(self):
        total_time = self.graduado_date - self.begin_date
        years = total_time.days / 365
        months = (total_time.days % 365) / (365 / 12.)

        # Texto
        plural = 's' if years > 1 else ''

        if months <= 3:
            return '%d año%s' % (years, plural)
        if months <= 7:
            return '%d 1/2 año%s' % (years, plural)
        else:
            return '%d año%s' % ((years + 1), plural)

    class Meta:
        unique_together = (('user', 'plancarrera'),)


class AlumnoMateria(models.Model):
    CUATRIMESTRES = (
        ('1', '1'),
        ('2', '2'),
        ('V', _('Verano')),
    )

    MATERIA_STATE = (
        ('-', _('No cursando')),
        ('C', _('Cursando')),
        ('F', _('Cursada Aprobada')),
        ('A', _('Materia Aprobada')),
        ('E', _('Equivalencia')),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    materia = models.ForeignKey('Materia', on_delete=models.CASCADE)
    state = models.CharField(choices=MATERIA_STATE, default='C', max_length=1)
    cursada_cuat = models.CharField(max_length=10, null=True, blank=True)
    cursada_date = models.DateField(null=True, blank=True)
    aprobada_cuat = models.CharField(max_length=10, null=True, blank=True)
    aprobada_date = models.DateField(null=True, blank=True)
    nota = models.IntegerField(null=True, default=0)
    creation_date = models.DateTimeField(auto_now_add=True)

    objects = AlumnoMateriaManager()

    def __str__(self):
        return '%s/%s' % (self.user, self.materia)

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
            return _('Curso de verano %(year)s') % ({'year': year})
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
        dict_aprobada_month = {1: '2', 2: '2', 3: '2', 4: '2', 5: '2',
                               6: '1', 7: '1', 8: '1', 9: '1', 10: '1',
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
        dict_cursada_month = {1: 'V', 2: 'V',
                              3: '1', 4: '1', 5: '1', 6: '1', 7: '1',
                              8: '2', 9: '2', 10: '2', 11: '2', 12: '2'}
        cuatrimestre = dict_cursada_month.get(self.cursada_date.month, '?')
        self.cursada_cuat = '%s-%s' % (cuatrimestre, self.cursada_date.year)

    class Meta:
        unique_together = (('user', 'materia'),)


class Carrera(models.Model):
    codigo = models.CharField(max_length=5)
    name = models.CharField(max_length=100)
    abbr_name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=20)
    plan_vigente = models.ForeignKey('PlanCarrera', related_name='plan',
                                     null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.short_name

    class Meta:
        ordering = ['name']


class PlanCarrera(models.Model):
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    pub_date = models.DateField()
    orientacion = models.CharField(max_length=255, null=True, blank=True)
    abbr_name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=20)
    min_creditos = models.IntegerField('Créditos')

    def __str__(self):
        return self.name

    def url_materias(self):
        return reverse('facultad:materias-carrera', args=[self.short_name])

    class Meta:
        ordering = ['name']


class Departamento(models.Model):
    codigo = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    vigente = models.BooleanField(default=True)

    def __str__(self):
        return self.codigo

    class Meta:
        ordering = ['codigo']


class Materia(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.id

    def get_codigo(self):
        return '%s.%s' % (self.departamento, self.codigo)
    get_codigo.short_description = 'Codigo'

    def get_name(self):
        return '%s.%s %s' % (self.departamento, self.codigo, self.name)

    def url_edit_materia(self):
        return reverse('facultad:materia', args=[self.id])

    class Meta:
        unique_together = (('departamento', 'codigo'),)
        ordering = ('departamento', 'codigo')


class PlanMateria(models.Model):
    plancarrera = models.ForeignKey(PlanCarrera, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    creditos = models.IntegerField()
    cuatrimestre = models.IntegerField()
    caracter = models.CharField(max_length=3)
    correlativas = models.CharField(max_length=255, null=True, blank=True)
    vigente = models.BooleanField(default=True)

    objects = PlanMateriaManager()

    def __str__(self):
        return '%s/%s' % (self.plancarrera, self.materia)

    class Meta:
        ordering = ['plancarrera', 'materia']


class Correlativa(models.Model):
    materia = models.ForeignKey(PlanMateria, related_name='materia_p',
                                on_delete=models.CASCADE)
    correlativa = models.ForeignKey(PlanMateria, related_name='correlativa',
                                    null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.materia)
