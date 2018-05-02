# -*- coding: utf-8 -*-
from django.db import models
from django.urls import reverse

from .managers import PlanMateriaManager


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

    class Meta:
        ordering = ['plancarrera', 'materia']


class Correlativa(models.Model):
    materia = models.ForeignKey(PlanMateria, related_name='materia_p',
                                on_delete=models.CASCADE)
    correlativa = models.ForeignKey(PlanMateria, related_name='correlativa',
                                    null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.materia
