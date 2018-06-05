import json

from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.test import APIClient
from test_plus.test import TestCase

from fiubar.facultad.models import (Alumno, AlumnoMateria, Materia,
                                    PlanCarrera, PlanMateria)


class FacultadBaseTest(TestCase):
    fixtures = ['fiubar']
    base_url = '/api/facultad/'

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.user = self.make_user()
        self.detail_url = self.base_url + '{}/'

    def create_new_alumno(self):
        pc1 = PlanCarrera.objects.get(id=4)
        a1 = Alumno.objects.create(user=self.user, carrera=pc1.carrera,
                                   plancarrera=pc1,
                                   begin_date='2013-03-01')

        pc2 = PlanCarrera.objects.get(id=14)
        a2 = Alumno.objects.create(user=self.user, carrera=pc2.carrera,
                                   plancarrera=pc2,
                                   begin_date='2013-08-01')

        pm = PlanMateria.objects.filter(plancarrera=pc2)
        AlumnoMateria.objects.create(user=self.user, materia=pm[0].materia,
                                     state='A', nota=9)
        AlumnoMateria.objects.create(user=self.user, materia=pm[8].materia,
                                     state='A', nota=8)
        AlumnoMateria.objects.create(user=self.user, materia=pm[2].materia,
                                     state='A', nota=4)
        AlumnoMateria.objects.create(user=self.user, materia=pm[20].materia,
                                     state='C')
        AlumnoMateria.objects.update_creditos(self.user, [a1, a2])


class UserApiTest(TestCase):

    def test_get_returns_json_404(self):
        self.user = self.make_user('admin', 'password', ['accounts.*'])
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


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
                "short_name": "agrimensura2"}
        response = self.client.post(self.base_url, data, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response['content-type'], 'application/json')

    def test_delete_carreras(self):
        carrera_id = 4
        response = self.client.delete(self.detail_url.format(carrera_id))
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response['content-type'], 'application/json')


class FacultadCarreraPlanCarreraAPITest(FacultadBaseTest):

    base_url = '/api/facultad/carreras/{}/plancarreras/'

    def test_get_plancarreras_quimica_2planes(self):
        carrera_id = 8
        response = self.client.get(self.base_url.format(carrera_id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')

        plan_carreras = json.loads(response.content.decode('utf8'))
        self.assertEqual(len(plan_carreras), 2)

    def test_get_planplan_carreras_informatica_orientacion(self):
        carrera_id = 10
        response = self.client.get(self.base_url.format(carrera_id))
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
        carrera_id = 8
        response = self.client.post(self.base_url.format(carrera_id),
                                    data, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response['content-type'], 'application/json')

    def test_delete_plancarreras(self):
        carrera_id = 8
        response = self.client.delete(self.base_url.format(carrera_id))
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response['content-type'], 'application/json')


class FacultadPlanCarreraPlanMateriaAPITest(FacultadBaseTest):

    base_url = '/api/facultad/plancarreras/{}/planmaterias/'

    def test_get_planmaterias_quimica(self):
        plancarrera_id = 8
        response = self.client.get(self.base_url.format(plancarrera_id))
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
        plancarrera_id = 8
        response = self.client.post(self.base_url.format(plancarrera_id),
                                    data, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response['content-type'], 'application/json')

    def test_delete_planmaterias(self):
        plancarrera_id = 8
        response = self.client.delete(self.base_url.format(plancarrera_id))
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response['content-type'], 'application/json')


class AlumnosAPITest(FacultadBaseTest):

    base_url = '/api/alumnos/plancarreras/'

    def test_get_alumnos_no_auth(self):
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response['content-type'], 'application/json')

    def test_get_alumnos_ok_auth(self):
        self.client.force_login(self.user)
        assert self.user.is_authenticated

        self.create_new_alumno()

        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')

        plan_carreras = json.loads(response.content.decode('utf8'))
        self.assertEqual(len(plan_carreras), 2)
        self.assertEqual(plan_carreras[0]['plancarrera'], 4)
        self.assertEqual(plan_carreras[0]['creditos'], 16)
        self.assertEqual(plan_carreras[0]['promedio'], 8.5)
        self.assertEqual(plan_carreras[1]['plancarrera'], 14)
        self.assertEqual(plan_carreras[1]['creditos'], 24)
        self.assertEqual(plan_carreras[1]['promedio'], 7.0)

    def test_get_alumnos_other_user(self):
        self.client.force_login(self.user)
        assert self.user.is_authenticated

        self.create_new_alumno()

        user2 = self.make_user('user2')
        pc = PlanCarrera.objects.get(id=4)
        a = Alumno.objects.create(user=user2, carrera=pc.carrera,
                                  plancarrera=pc,
                                  begin_date='2013-03-01')

        response = self.client.get(self.detail_url.format(a.id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.client.force_login(user2)
        assert user2.is_authenticated

        response = self.client.get(self.detail_url.format(a.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_alumnos_detail_404(self):
        self.client.force_login(self.user)
        assert self.user.is_authenticated

        self.create_new_alumno()

        alumno_id = 10
        response = self.client.get(self.detail_url.format(alumno_id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_alumnos_detail_ok(self):
        self.client.force_login(self.user)
        assert self.user.is_authenticated

        self.create_new_alumno()

        alumno_id = 1
        response = self.client.get(self.detail_url.format(alumno_id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')

        plan_carrera = json.loads(response.content.decode('utf8'))
        self.assertEqual(len(plan_carrera), 9)
        self.assertEqual(plan_carrera['plancarrera'], 4)
        self.assertEqual(plan_carrera['creditos'], 16)
        self.assertEqual(plan_carrera['promedio'], 8.5)

    def test_post_alumnos_no_auth(self):
        response = self.client.post(self.base_url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response['content-type'], 'application/json')

    def test_post_alumnos_bad_data(self):
        self.client.force_login(self.user)
        assert self.user.is_authenticated

        self.create_new_alumno()

        data = {"user": self.user.id}
        response = self.client.post(self.base_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response['content-type'], 'application/json')

        errors = json.loads(response.content.decode('utf8'))
        self.assertEqual(len(errors), 2)
        self.assertTrue('carrera' in errors.keys())
        self.assertTrue('plancarrera' in errors.keys())

    def test_post_alumnos_bad_carrera(self):
        self.client.force_login(self.user)
        assert self.user.is_authenticated

        self.create_new_alumno()

        data = {"user": self.user.id,
                "begin_date": "2017-04-02",
                "carrera": 200,
                "plancarrera": 314}
        response = self.client.post(self.base_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response['content-type'], 'application/json')

        errors = json.loads(response.content.decode('utf8'))
        self.assertEqual(len(errors), 2)
        self.assertTrue('carrera' in errors.keys())
        self.assertTrue('plancarrera' in errors.keys())

    def test_post_alumnos_ok(self):
        self.client.force_login(self.user)
        assert self.user.is_authenticated

        self.create_new_alumno()

        data = {"user": self.user.id,
                "begin_date": "2017-04-02",
                "carrera": 10,
                "plancarrera": 16}
        response = self.client.post(self.base_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response['content-type'], 'application/json')

        plan_carrera = json.loads(response.content.decode('utf8'))
        self.assertEqual(len(plan_carrera), 9)
        self.assertEqual(plan_carrera['user'], 1)
        self.assertEqual(plan_carrera['carrera'], 10)
        self.assertEqual(plan_carrera['plancarrera'], 16)
        self.assertEqual(plan_carrera['creditos'], 24)
        self.assertEqual(plan_carrera['promedio'], 7.0)

    def test_delete_alumnos_no_auth(self):
        alumno_id = 1
        response = self.client.delete(self.detail_url.format(alumno_id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response['content-type'], 'application/json')

    def test_delete_alumnos_ok_auth(self):
        self.client.force_login(self.user)
        assert self.user.is_authenticated

        self.create_new_alumno()

        alumno_id = 1
        response = self.client.delete(self.detail_url.format(alumno_id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b'')

        response = self.client.get(self.detail_url.format(alumno_id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_alumnos_no_auth(self):
        alumno_id = 1
        response = self.client.put(self.detail_url.format(alumno_id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response['content-type'], 'application/json')

    def test_put_alumnos_invalid_plancarrera(self):
        self.client.force_login(self.user)
        assert self.user.is_authenticated

        self.create_new_alumno()

        data = {"user": self.user.id,
                "begin_date": "2017-04-02",
                "carrera": 1,
                "plancarrera": 16}
        alumno_id = 1

        # Este test no deberia dar ValidationError, sino un HTTP code.
        # Ver https://github.com/maru/fiubar/issues/
        with self.assertRaises(ValidationError):
            self.client.put(self.detail_url.format(alumno_id),
                            data, format='json')

    def test_put_alumnos_ok_auth(self):
        self.client.force_login(self.user)
        assert self.user.is_authenticated

        self.create_new_alumno()

        data = {"user": self.user.id,
                "begin_date": "2017-04-02",
                "carrera": 10,
                "plancarrera": 16}
        alumno_id = 1
        response = self.client.put(self.detail_url.format(alumno_id),
                                   data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')

        plan_carrera = json.loads(response.content.decode('utf8'))
        self.assertEqual(len(plan_carrera), 9)
        self.assertEqual(plan_carrera['carrera'], 10)
        self.assertEqual(plan_carrera['plancarrera'], 16)
        self.assertEqual(plan_carrera['creditos'], 16)
        self.assertEqual(plan_carrera['promedio'], 8.5)


class AlumnoMateriasAPITest(FacultadBaseTest):

    base_url = '/api/alumnos/materias/'

    def test_get_alumnomaterias_no_auth(self):
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response['content-type'], 'application/json')

    def test_get_alumnomaterias_ok_auth(self):
        self.client.force_login(self.user)
        assert self.user.is_authenticated

        self.create_new_alumno()

        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')

        materias = json.loads(response.content.decode('utf8'))
        self.assertEqual(len(materias), 4)
        self.assertEqual(materias[0]['materia'], '6103')
        self.assertEqual(materias[0]['state'], 'A')
        self.assertEqual(materias[0]['nota'], 9)
        self.assertEqual(materias[1]['materia'], '6203')
        self.assertEqual(materias[1]['state'], 'A')
        self.assertEqual(materias[1]['nota'], 8)
        self.assertEqual(materias[2]['materia'], '6108')
        self.assertEqual(materias[2]['state'], 'A')
        self.assertEqual(materias[2]['nota'], 4)
        self.assertEqual(materias[3]['materia'], '6620')
        self.assertEqual(materias[3]['state'], 'C')
        self.assertEqual(materias[3]['nota'], 0)

    def test_get_alumnomaterias_other_user(self):
        self.client.force_login(self.user)
        assert self.user.is_authenticated

        self.create_new_alumno()

        user2 = self.make_user('user2')
        m = Materia.objects.get(id='6103')
        a = AlumnoMateria.objects.create(user=user2, materia=m, state='A')

        response = self.client.get(self.detail_url.format(a.id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.client.force_login(user2)
        assert user2.is_authenticated

        response = self.client.get(self.detail_url.format(a.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_alumnomaterias_detail_404(self):
        self.client.force_login(self.user)
        assert self.user.is_authenticated

        self.create_new_alumno()

        materia_id = 10
        response = self.client.get(self.detail_url.format(materia_id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_alumnomaterias_detail_ok(self):
        self.client.force_login(self.user)
        assert self.user.is_authenticated

        self.create_new_alumno()

        materia_id = 1
        response = self.client.get(self.detail_url.format(materia_id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')

        materia = json.loads(response.content.decode('utf8'))
        self.assertEqual(len(materia), 10)
        self.assertEqual(materia['materia'], '6103')
        self.assertEqual(materia['state'], 'A')
        self.assertEqual(materia['nota'], 9)

    def test_post_alumnomaterias_no_auth(self):
        response = self.client.post(self.base_url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response['content-type'], 'application/json')

    def test_post_alumnomaterias_bad_data(self):
        self.client.force_login(self.user)
        assert self.user.is_authenticated

        self.create_new_alumno()

        data = {"user": self.user.id}
        response = self.client.post(self.base_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response['content-type'], 'application/json')

        errors = json.loads(response.content.decode('utf8'))
        self.assertEqual(len(errors), 1)
        self.assertListEqual(['materia'], list(errors.keys()))

    def test_post_alumnomaterias_bad_materia(self):
        self.client.force_login(self.user)
        assert self.user.is_authenticated

        self.create_new_alumno()

        data = {"user": self.user.id,
                "materia": "16109"}
        response = self.client.post(self.base_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response['content-type'], 'application/json')

        errors = json.loads(response.content.decode('utf8'))
        self.assertEqual(len(errors), 1)
        self.assertListEqual(['materia'], list(errors.keys()))

    def test_post_alumnomaterias_ok(self):
        self.client.force_login(self.user)
        assert self.user.is_authenticated

        self.create_new_alumno()

        data = {"user": self.user.id,
                "materia": "6109"}
        response = self.client.post(self.base_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response['content-type'], 'application/json')

        materia = json.loads(response.content.decode('utf8'))
        self.assertEqual(len(materia), 10)
        self.assertEqual(materia['user'], 1)
        self.assertEqual(materia['state'], 'C')
        self.assertEqual(materia['materia'], '6109')

    def test_delete_alumnomaterias_no_auth(self):
        materia_id = 1
        response = self.client.delete(self.detail_url.format(materia_id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response['content-type'], 'application/json')

    def test_delete_alumnomaterias_ok_auth(self):
        self.client.force_login(self.user)
        assert self.user.is_authenticated

        self.create_new_alumno()

        materia_id = 1
        response = self.client.delete(self.detail_url.format(materia_id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b'')

        response = self.client.get(self.detail_url.format(materia_id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_alumnomaterias_no_auth(self):
        materia_id = 1
        response = self.client.put(self.detail_url.format(materia_id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response['content-type'], 'application/json')

    def test_put_alumnomaterias_invalid_materia(self):
        self.client.force_login(self.user)
        assert self.user.is_authenticated

        self.create_new_alumno()

        data = {"user": self.user.id,
                "materia": "1234"}
        materia_id = 1

        response = self.client.put(self.detail_url.format(materia_id),
                                   data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_alumnomaterias_ok_auth(self):
        self.client.force_login(self.user)
        assert self.user.is_authenticated

        self.create_new_alumno()

        data = {"user": self.user.id,
                "state": 'E',
                "materia": "7501"}
        materia_id = 1
        response = self.client.put(self.detail_url.format(materia_id),
                                   data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')

        materia = json.loads(response.content.decode('utf8'))
        self.assertEqual(len(materia), 10)
        self.assertEqual(materia['user'], 1)
        self.assertEqual(materia['state'], 'E')
        self.assertEqual(materia['materia'], '7501')
