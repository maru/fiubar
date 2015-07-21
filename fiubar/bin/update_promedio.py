# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from facultad.models import Carrera, Alumno, AlumnoMateria, PlanCarrera

alumnos = Alumno.objects.all()
#AlumnoMateria.objects.update_creditos(user, alumnos)
#def update_creditos(self, user, list_carreras):
from facultad.models import PlanMateria

for al in alumnos:
	materias_cursadas = AlumnoMateria.objects.filter(user=al.user)
	# Recalculo los creditos para cada carrera
	creditos = 0
	promedio = 0.0
	count_materias = 0
	for m in materias_cursadas:
		if not (m.aprobada() or m.equivalencia()):
			continue
		# Check si materia existe en carrera
		materia = PlanMateria.objects.filter(plancarrera=al.plancarrera, materia=m.materia)
		# Update de creditos en carrera
		if materia.count():
			creditos += materia[0].creditos
			if m.nota > 0:
				promedio += m.nota
				count_materias += 1
	if count_materias:
		promedio = round(promedio / count_materias, 2)
	if al.creditos != creditos or al.promedio != promedio:
		print al.user, ': ', al.creditos, '<>', creditos, al.promedio, '<>', promedio
		al.creditos = creditos
		al.promedio = promedio
		al.save()
		print al.user, ': ', al.creditos, '<>', creditos, al.promedio, '<>', promedio


