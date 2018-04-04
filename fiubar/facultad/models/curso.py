# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin

"MateriaCurso"
class MateriaCurso(models.Model):
	materia  = models.ForeignKey(Materia, on_delete=models.CASCADE)
	codigo   = models.CharField(max_length=10)
	vacantes = models.IntegerField()
	docentes = models.CharField(max_length=100)
	carreras = models.CharField(max_length=50)
	horarios = models.TextField()
	pub_date = models.DateField()

    def __str__(self):
        return self.materia

    @admin.register(MateriaCurso)
	class Admin(admin.ModelAdmin):
		list_display = ['materia', 'codigo', 'vacantes', 'docentes', 'carreras', 'horarios', 'pub_date']
		search_fields = ('materia__id', 'materia__name', 'docentes', 'horarios')


"HorarioCurso"
class HorarioCurso(models.Model):
	curso     = models.ForeignKey(MateriaCurso, on_delete=models.CASCADE)
	modalidad = models.CharField(max_length=1)
	dia       = models.CharField(max_length=1)
	desde     = models.CharField(max_length=1)
	hasta     = models.CharField(max_length=1)


"DocenteCurso"
class DocenteCurso(models.Model):
	docente = models.CharField(max_length=1)
	horario = models.CharField(max_length=1)
