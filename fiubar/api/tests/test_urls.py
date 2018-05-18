# import json

from test_plus.test import TestCase

from fiubar.facultad.models import Carrera


class UserApiTest(TestCase):

    def setUp(self):
        self.user = self.make_user('admin', 'password', ['users'])
        self.user.set_password()

    def test_get_returns_json_200(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, 404)


class FacultadCarreraAPITest(TestCase):
    base_url = '/api/facultad/carreras/{}/'

    def _test_get_returns_json_200(self):
        carrera = Carrera.objects.create()
        response = self.client.get(self.base_url.format(carrera.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
