# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import (Alumno, AlumnoMateria,Carrera, Correlativa, Departamento,
                     Materia, PlanCarrera, PlanMateria)


@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ['user', 'carrera', 'plancarrera', 'begin_date',
                    'graduado_date', 'promedio', 'creditos',
                    'creation_date']


@admin.register(AlumnoMateria)
class AlumnoMateriaAdmin(admin.ModelAdmin):
    list_display = ['user', 'materia', 'state', 'cursada_cuat',
                    'cursada_date', 'aprobada_cuat', 'aprobada_date']
    list_filter = ['cursada_cuat', 'aprobada_cuat', 'state']
    search_fields = ['user__username', 'user__first_name',
                     'user__last_name', 'user__email',
                     'materia__id', 'materia__name']

@admin.register(Carrera)
class CarreraAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbr_name', 'short_name',
                    'codigo', 'plan_vigente')


@admin.register(PlanCarrera)
class PlanCarreraAdmin(admin.ModelAdmin):
    list_display = ('name', 'carrera', 'orientacion', 'abbr_name',
                    'short_name', 'pub_date', 'min_creditos')


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'name', 'vigente')
    list_display_links = ('codigo', 'name')


@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ('departamento', 'codigo', 'get_codigo', 'name')
    list_display_links = ('departamento', 'codigo', 'get_codigo', 'name')
    list_filter = ('departamento',)
    search_fields = ('name', 'departamento__codigo', 'codigo', )


@admin.register(PlanMateria)
class PlanMateriaAdmin(admin.ModelAdmin):
    list_display = ('materia', 'plancarrera', 'creditos', 'cuatrimestre',
                    'caracter', 'correlativas', 'vigente')
    list_filter = ['plancarrera', 'vigente']
    list_per_page = 20


@admin.register(Correlativa)
class CorrelativaAdmin(admin.ModelAdmin):
    list_display = ('materia', 'correlativa')
