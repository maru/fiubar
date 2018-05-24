from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .permissions import IsAuthenticatedOwner

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
    queryset = Alumno.objects.none()
    serializer_class = AlumnoSerializer
    permission_classes = [IsAuthenticatedOwner]

    def get_queryset(self):
        self.queryset = Alumno.objects.filter(user=self.request.user)\
            .order_by('carrera')
        return super(AlumnoViewSet, self).get_queryset()


class AlumnoMateriaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows alumnomaterias to be viewed or edited.
    """
    queryset = AlumnoMateria.objects.none()
    serializer_class = AlumnoMateriaSerializer
    permission_classes = [IsAuthenticatedOwner]

    def get_queryset(self):
        self.queryset = AlumnoMateria.objects.filter(user=self.request.user)
        return super(AlumnoMateriaViewSet, self).get_queryset()


class FacultadAPIView(viewsets.ReadOnlyModelViewSet):
    pass


class CarreraViewSet(FacultadAPIView):
    """
    API endpoint that allows Carrera to be viewed or edited.
    """
    queryset = Carrera.objects.all()
    serializer_class = CarreraSerializer

    @api_view(['GET'])
    def get_plancarreras(self, pk, *args, **kwargs):
        pc_list = PlanCarrera.objects.filter(carrera=pk)
        serializer = PlanCarreraSerializer(pc_list, many=True)
        return Response(serializer.data)


class CorrelativaViewSet(FacultadAPIView):
    """
    API endpoint that allows Correlativa to be viewed or edited.
    """
    queryset = Correlativa.objects.all()
    serializer_class = CorrelativaSerializer


class DepartamentoViewSet(FacultadAPIView):
    """
    API endpoint that allows Departamento to be viewed or edited.
    """
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer


class MateriaViewSet(FacultadAPIView):
    """
    API endpoint that allows Materia to be viewed or edited.
    """
    queryset = Materia.objects.all()
    serializer_class = MateriaSerializer


class PlanCarreraViewSet(FacultadAPIView):
    """
    API endpoint that allows PlanCarrera to be viewed or edited.
    """
    queryset = PlanCarrera.objects.all()
    serializer_class = PlanCarreraSerializer

    @api_view(['GET'])
    def get_planmaterias(self, pk, *args, **kwargs):
        pm_list = PlanMateria.objects.select_related('materia')\
            .filter(plancarrera=pk)
        serializer = PlanMateriaSerializer(pm_list, many=True)
        return Response(serializer.data)


class PlanMateriaViewSet(FacultadAPIView):
    """
    API endpoint that allows PlanMateria to be viewed or edited.
    """
    queryset = PlanMateria.objects.all()
    serializer_class = PlanMateriaSerializer
