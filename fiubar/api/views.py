from rest_framework import viewsets

from fiubar.api.serializers import (AlumnoMateriaSerializer, AlumnoSerializer,
                                    CarreraSerializer, CorrelativaSerializer,
                                    DepartamentoSerializer, MateriaSerializer,
                                    PlanCarreraSerializer,
                                    PlanMateriaSerializer)
from fiubar.facultad.models import (Alumno, AlumnoMateria, Carrera,
                                    Correlativa, Departamento, Materia,
                                    PlanCarrera, PlanMateria)


class AlumnoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows alumnos to be viewed or edited.
    """
    queryset = Alumno.objects.all().order_by('carrera')
    serializer_class = AlumnoSerializer


class AlumnoMateriaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows alumnomaterias to be viewed or edited.
    """
    queryset = AlumnoMateria.objects.all()
    serializer_class = AlumnoMateriaSerializer


class CarreraViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Carrera to be viewed or edited.
    """
    queryset = Carrera.objects.all()
    serializer_class = CarreraSerializer


class CorrelativaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Correlativa to be viewed or edited.
    """
    queryset = Correlativa.objects.all()
    serializer_class = CorrelativaSerializer


class DepartamentoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Departamento to be viewed or edited.
    """
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer


class MateriaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Materia to be viewed or edited.
    """
    queryset = Materia.objects.all()
    serializer_class = MateriaSerializer


class PlanCarreraViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows PlanCarrera to be viewed or edited.
    """
    queryset = PlanCarrera.objects.all()
    serializer_class = PlanCarreraSerializer


class PlanMateriaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows PlanMateria to be viewed or edited.
    """
    queryset = PlanMateria.objects.all()
    serializer_class = PlanMateriaSerializer
