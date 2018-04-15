# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext as _
from fiubar.users.models import User

from .functions import calculate_time
from .managers import AlumnoManager, AlumnoMateriaManager, PlanMateriaManager


# -*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*-
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


# -*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*-
class AlumnoMateria(models.Model):
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    materia = models.ForeignKey('Materia', on_delete=models.CASCADE)
    state = models.CharField(choices=MATERIA_STATE, default='C', max_length=1)
    cursada_cuat = models.CharField(max_length=10, null=True, blank=True)
    cursada_date = models.DateField(null=True, blank=True)
    aprobada_cuat = models.CharField(max_length=10, null=True, blank=True)
    aprobada_date = models.DateField(null=True, blank=True)
    nota = models.IntegerField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    objects = AlumnoMateriaManager()

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


# -*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*-
class Carrera(models.Model):
    codigo = models.CharField(max_length=5)
    name = models.CharField(max_length=100)
    abbr_name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=20)
    plan_vigente = models.ForeignKey('PlanCarrera', related_name='plan',
                                     null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.short_name

    def url_materias(self):
        return reverse('facultad:materias-carrera', args=[self.short_name])

    def url_alumnos(self):
        return reverse('facultad:carrera-alumnos', args=[self.short_name])

    class Meta:
        ordering = ['name']

    class Admin(admin.ModelAdmin):
        list_display = ('name', 'abbr_name', 'short_name',
                        'codigo', 'plan_vigente')


# -*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*-
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

    class Admin(admin.ModelAdmin):
        list_display = ('name', 'carrera', 'orientacion', 'abbr_name',
                        'short_name', 'pub_date', 'min_creditos')


# -*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*-
class PlanOrientacion(models.Model):
    plancarrera = models.ForeignKey(PlanCarrera, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return 'R%s' % (self.id)
        return '%s %s' % (self.get_codigo, self.name)

    def get_codigo(self):
        return 'R%s' % (self.id)

    class Admin(admin.ModelAdmin):
        list_display = ('get_codigo', 'plancarrera', 'name', 'descripcion')
        list_display_links = ('get_codigo', 'name', )

    class Meta:
        pass


# -*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*-
class Departamento(models.Model):
    codigo = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    vigente = models.BooleanField(default=True)

    def __str__(self):
        return self.codigo

    class Meta:
        ordering = ['codigo']

    class Admin(admin.ModelAdmin):
        list_display = ('codigo', 'name', 'vigente')
        list_display_links = ('codigo', 'name')


# -*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*-
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

    def url_home(self):
        return reverse('facultad:materia-show', args=[self.id])

    def url_encuestas(self):
        return reverse('facultad:materia-encuesta', args=[self.id])

    def url_files(self):
        return self.url_files_path() + '/'

    def url_files_path(self):
        return '/materias/%s/files' % self.id

    def url_group(self):
        return reverse('facultad:materia-group', args=[self.id])

    def url_group_subscription(self):
        return reverse('facultad:group-settings', args=[self.group_name()])

    def url_alumnos(self):
        return reverse('facultad:materia-cursos', args=[self.id])

    def url_events(self):
        return reverse('facultad:materia-events', args=[self.id])

    def url_events_add(self):
        return reverse('facultad:materia-events_add', args=[self.id])

    def group_name(self):
        return 'fiuba-%s' % self.id

    def url_edit_materia(self):
        return reverse('facultad:materia', args=[self.id])

    class Meta:
        unique_together = (('departamento', 'codigo'),)
        ordering = ('departamento', 'codigo')

    class Admin(admin.ModelAdmin):
        list_display = ('departamento', 'codigo', 'get_codigo', 'name')
        list_display_links = ('departamento', 'codigo', 'get_codigo', 'name')
        list_filter = ('departamento',)
        search_fields = ('name', 'departamento__codigo', 'codigo', )


# -*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*-
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

    def url_edit_materia(self):
        return reverse('facultad:materia', args=[self.materia])

    class Admin(admin.ModelAdmin):
        list_display = ('materia', 'plancarrera', 'creditos', 'cuatrimestre',
                        'caracter', 'correlativas', 'vigente')
        list_filter = ['plancarrera', 'vigente']
        list_per_page = 20

    class Meta:
        ordering = ['plancarrera', 'materia']


class Correlativa(models.Model):
    materia = models.ForeignKey(PlanMateria, related_name='materia_p',
                                on_delete=models.CASCADE)
    correlativa = models.ForeignKey(PlanMateria, related_name='correlativa',
                                    null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.materia

    class Admin(admin.ModelAdmin):
        list_display = ('materia', 'correlativa')


# -*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*-
class MateriaExcluyente(models.Model):
    name = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return 'X%s' % (self.id)
        return '%s %s' % (self.get_codigo, self.name)

    def get_codigo(self):
        return 'X%s' % (self.id)

    class Admin(admin.ModelAdmin):
        list_display = ('get_codigo', 'name', 'descripcion')

    class Meta:
        pass
