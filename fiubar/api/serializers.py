from rest_framework import serializers

from fiubar.facultad.models import (Alumno, AlumnoMateria, Carrera,
                                    Correlativa, Departamento, Materia,
                                    PlanCarrera, PlanMateria)


class AlumnoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Alumno
        # fields = ('user', 'carrera', 'plancarrera', 'begin_date', )


class AlumnoMateriaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AlumnoMateria
        # fields = ('url', 'name')


class CarreraSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Carrera


class CorrelativaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Correlativa


class DepartamentoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Departamento


class MateriaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Materia


class PlanCarreraSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PlanCarrera


class PlanMateriaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PlanMateria
