from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import permissions
from .permissions import IsOwner


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
    permission_classes = (permissions.IsAuthenticated, IsOwner)


class AlumnoMateriaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows alumnomaterias to be viewed or edited.
    """
    queryset = AlumnoMateria.objects.all()
    serializer_class = AlumnoMateriaSerializer
    permission_classes = (permissions.IsAuthenticated,)


class FacultadAPIView(viewsets.ReadOnlyModelViewSet):
    pass

class CarreraViewSet(FacultadAPIView):
    """
    API endpoint that allows Carrera to be viewed or edited.
    """
    queryset = Carrera.objects.all()
    serializer_class = CarreraSerializer

    @csrf_exempt
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

    @csrf_exempt
    @api_view(['GET'])
    def get_planmaterias(self, pk, *args, **kwargs):
        pm_list = PlanMateria.objects.select_related('materia').filter(plancarrera=pk)
        serializer = PlanMateriaSerializer(pm_list, many=True)
        return Response(serializer.data)


class PlanMateriaViewSet(FacultadAPIView):
    """
    API endpoint that allows PlanMateria to be viewed or edited.
    """
    queryset = PlanMateria.objects.all()
    serializer_class = PlanMateriaSerializer
