from rest_framework import serializers

from fiubar.facultad.models import (Alumno, AlumnoMateria, Carrera,
                                    Correlativa, Departamento, Materia,
                                    PlanCarrera, PlanMateria)
from fiubar.users.models import User


class AlumnoSerializer(serializers. ModelSerializer):
    class Meta:
        model = Alumno
        exclude = []


class AlumnoMateriaSerializer(serializers. ModelSerializer):
    class Meta:
        model = AlumnoMateria
        exclude = []


class DepartamentoSerializer(serializers. ModelSerializer):
    class Meta:
        model = Departamento
        exclude = []


class MateriaSerializer(serializers. ModelSerializer):
    class Meta:
        model = Materia
        exclude = ['departamento', 'codigo']


class PlanMateriaSerializer(serializers. ModelSerializer):
    materia = MateriaSerializer(read_only=True)
    class Meta:
        model = PlanMateria
        exclude = []


class PlanCarreraSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanCarrera
        exclude = []


class CarreraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrera
        exclude = []


class CorrelativaSerializer(serializers. ModelSerializer):
    class Meta:
        model = Correlativa
        exclude = []
