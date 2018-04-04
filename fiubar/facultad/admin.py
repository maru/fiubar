# -*- coding: utf-8 -*-

from django.contrib import admin

from .models.models import Alumno, AlumnoMateria

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
