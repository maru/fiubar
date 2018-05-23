import json

from rest_framework import status
from rest_framework.test import APIClient
from test_plus.test import TestCase

from fiubar.facultad.models import Carrera


class APITestCase(TestCase):
    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()

class UserApiTest(APITestCase):

    def test_get_returns_json_404(self):
        self.user = self.make_user('admin', 'password', ['accounts.*'])
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class FacultadBaseTest(APITestCase):
    fixtures = ['fiubar']


class FacultadCarreraAPITest(FacultadBaseTest):
    base_url = '/api/facultad/carreras/'

    def test_get_carreras(self):
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')

        carreras = json.loads(response.content.decode('utf8'))
        self.assertEqual(len(carreras), 12)

    def test_post_carreras(self):
        data = {"codigo": "40",
                "name": "Agrimensura2",
                "abbr_name": "Agrimensura2",
                "short_name": "agrimensura2",}
        response = self.client.post(self.base_url, data, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response['content-type'], 'application/json')

    def test_delete_carreras(self):
        response = self.client.delete(self.base_url + '4/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response['content-type'], 'application/json')


class FacultadCarreraPlanCarreraAPITest(FacultadBaseTest):

    base_url = '/api/facultad/carreras/%s/plancarreras/'

    def test_get_plancarreras_quimica_2planes(self):
        response = self.client.get(self.base_url % '8')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')

        plan_carreras = json.loads(response.content.decode('utf8'))
        self.assertEqual(len(plan_carreras), 2)

    def test_get_planplan_carreras_informatica_orientacion(self):
        response = self.client.get(self.base_url % '10')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')

        plan_carreras = json.loads(response.content.decode('utf8'))
        self.assertEqual(len(plan_carreras), 4)

    def test_post_plancarreras(self):
        data = {"name": "Ingeniería Química Plan 2986",
                "pub_date": "2986-03-17",
                "orientacion": "Inorgánica",
                "abbr_name": "Ing. Química 2986",
                "short_name": "quimica2986",
                "min_creditos": 240,
                "carrera": 8}
        response = self.client.post(self.base_url % '8', data, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response['content-type'], 'application/json')

    def test_delete_plancarreras(self):
        response = self.client.delete(self.base_url % '8')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response['content-type'], 'application/json')


class FacultadPlanCarreraPlanMateriaAPITest(FacultadBaseTest):

    base_url = '/api/facultad/plancarreras/8/planmaterias/'

    def test_get_planmaterias_quimica(self):
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')

        materias = json.loads(response.content.decode('utf8'))
        self.assertEqual(len(materias), 67)


    def test_post_planmaterias(self):
        data = {"creditos": 8,
                "cuatrimestre": 3,
                "caracter": "O",
                "correlativas": "CBC",
                "vigente": True,
                "plancarrera": 8,
                "materia": "7503"}
        response = self.client.post(self.base_url, data, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response['content-type'], 'application/json')

    def test_delete_planmaterias(self):
        response = self.client.delete(self.base_url)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response['content-type'], 'application/json')



class AlumnosPlanCarreraAPITest(FacultadBaseTest):

    base_url = '/api/alumnos/'

    def test_get_alumnos_no_auth(self):
        response = self.client.get(self.base_url)
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response['content-type'], 'application/json')

    def test_get_alumnos_ok_auth(self):
        response = self.client.get(self.base_url)
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response['content-type'], 'application/json')

    def test_post_plancarreras(self):
        response = self.client.post(self.base_url)
        print(response.content)
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response['content-type'], 'application/json')

        plan_carreras = json.loads(response.content.decode('utf8'))
        self.assertEqual(len(plan_carreras), 2)

class AlumnosPlanCarreraAPITest(FacultadBaseTest):

    def test_get_materias(self):
        base_url = '/api/alumnos/materias/'
        response = self.client.get(base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')

        materias = json.loads(response.content.decode('utf8'))
        self.assertEqual(len(materias), 2)

    def test_post_materias(self):
        base_url = '/api/alumnos/materias/'
        response = self.client.post(base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')

        materias = json.loads(response.content.decode('utf8'))
        self.assertEqual(len(materias), 2)
