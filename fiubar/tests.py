from django.contrib.messages import constants as MSG
from django.core.exceptions import ObjectDoesNotExist
from django.test import RequestFactory
from django.urls import reverse
from django.utils.translation import ugettext as _
from test_plus.test import TestCase

from .forms import SignupForm

from fiubar.facultad.models import Alumno, AlumnoMateria
from fiubar.facultad.tests.common import BaseUserTestCase


class TestSignupForm(TestCase):

    def setUp(self):
        self.user = self.make_user()
        self.factory = RequestFactory()

    def test_signup(self):
        form = SignupForm({})
        del form.fields['captcha']

        # Run is_valid() to trigger the validation
        valid = form.is_valid()
        self.assertTrue(valid)

        # Generate a fake request
        request = self.factory.get('/fake-url')
        # Attach the user to the request
        request.user = self.user
        form.signup(request, self.user)


class TestHomeView(TestCase):

    def setUp(self):
        self.user = self.make_user(password='pwtest')

    def test_home_page_user(self):
        self.client.force_login(self.user)
        assert self.user.is_authenticated

        response = self.client.get('/', follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain,
                         [('/facultad/', 302)])

        self.assertTemplateUsed(response, 'facultad/home.html')

    def test_new_user(self):
        response = self.client.get('/', follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'new_user/index.html')


class TestCreateAlumnoHomeView(BaseUserTestCase):

    def test_no_cookies(self):
        response = self.client.post(reverse('account_login'),
                                    {'login': self.user.username,
                                     'password': self.user.password},
                                    follow=True)

        self.assertEqual(len(response.redirect_chain), 2)
        self.assertEqual(response.redirect_chain,
                         [(reverse('home'), 302),
                          (reverse('facultad:home'), 302)])

        self.assertIsNone(response.cookies.get('create_alumno'))
        self.assertIsNone(response.cookies.get('plancarrera'))
        self.assertIsNone(response.cookies.get('materias'))

    def test_create_alumno_cookie(self):
        a = Alumno.objects.filter(user=self.user)
        self.assertEqual(len(a), 4)
        self.client.cookies.load({'create_alumno': '1'})
        response = self.client.post(reverse('account_login'),
                                    {'login': self.user.username,
                                     'password': self.user.password},
                                    follow=True)

        self.assertEqual(len(response.redirect_chain), 2)
        self.assertEqual(response.redirect_chain,
                         [(reverse('home'), 302),
                          (reverse('facultad:home'), 302)])

        self.assertIsNone(response.cookies.get('create_alumno'))
        self.assertIsNone(response.cookies.get('plancarrera'))
        self.assertIsNone(response.cookies.get('materias'))

        a = Alumno.objects.filter(user=self.user)
        self.assertEqual(len(a), 4)

    def test_plancarrera_does_not_exist(self):
        a = Alumno.objects.filter(user=self.user)
        self.assertEqual(len(a), 4)
        self.client.cookies.load({'create_alumno': '1',
                                  'plancarrera': '{"id": 0}'})
        response = self.client.post(reverse('account_login'),
                                    {'login': self.user.username,
                                     'password': self.user.password},
                                    follow=True)

        self.assertEqual(len(response.redirect_chain), 2)
        self.assertEqual(response.redirect_chain,
                         [(reverse('home'), 302),
                          (reverse('facultad:home'), 302)])

        self.assertIsNone(response.cookies.get('create_alumno'))
        self.assertIsNone(response.cookies.get('plancarrera'))
        self.assertIsNone(response.cookies.get('materias'))

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 0)

        a = Alumno.objects.filter(user=self.user)
        self.assertEqual(len(a), 4)

    def test_plancarrera_ya_alumno(self):
        a = Alumno.objects.filter(user=self.user)
        self.assertEqual(len(a), 4)
        self.client.cookies.load({'create_alumno': '1',
                                  'plancarrera': '{"id": 1}'})
        response = self.client.post(reverse('account_login'),
                                    {'login': self.user.username,
                                     'password': self.user.password},
                                    follow=True)

        self.assertEqual(len(response.redirect_chain), 2)
        self.assertEqual(response.redirect_chain,
                         [(reverse('home'), 302),
                          (reverse('facultad:home'), 302)])

        self.assertIsNone(response.cookies.get('create_alumno'))
        self.assertIsNone(response.cookies.get('plancarrera'))
        self.assertIsNone(response.cookies.get('materias'))

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 0)

        a = Alumno.objects.filter(user=self.user)
        self.assertEqual(len(a), 4)

    def test_plancarrera_nuevo_alumno(self):
        a = Alumno.objects.filter(user=self.user)
        self.assertEqual(len(a), 4)
        self.client.cookies.load({'create_alumno': '1',
                                  'plancarrera': '{"id": 4}'})
        response = self.client.post(reverse('account_login'),
                                    {'login': self.user.username,
                                     'password': self.user.password},
                                    follow=True)

        self.assertEqual(len(response.redirect_chain), 2)
        self.assertEqual(response.redirect_chain,
                         [(reverse('home'), 302),
                          (reverse('facultad:home'), 302)])

        self.assertIsNone(response.cookies.get('create_alumno'))
        self.assertIsNone(response.cookies.get('plancarrera'))
        self.assertIsNone(response.cookies.get('materias'))

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].level, MSG.SUCCESS)
        self.assertEqual(messages[0].message, _('Carrera agregada.'))

        a = Alumno.objects.filter(user=self.user)
        self.assertEqual(len(a), 5)

    def test_materias_vacio(self):
        a = AlumnoMateria.objects.filter(user=self.user)
        self.assertEqual(len(a), 4)
        self.client.cookies.load({'create_alumno': '1',
                                  'plancarrera': '{"id": 4}',
                                  'materias': '{}'})
        response = self.client.post(reverse('account_login'),
                                    {'login': self.user.username,
                                     'password': self.user.password},
                                    follow=True)

        self.assertEqual(len(response.redirect_chain), 2)
        self.assertEqual(response.redirect_chain,
                         [(reverse('home'), 302),
                          (reverse('facultad:home'), 302)])

        self.assertIsNone(response.cookies.get('create_alumno'))
        self.assertIsNone(response.cookies.get('plancarrera'))
        self.assertIsNone(response.cookies.get('materias'))

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].level, MSG.SUCCESS)
        self.assertEqual(messages[0].message, _('Carrera agregada.'))

        a = AlumnoMateria.objects.filter(user=self.user)
        self.assertEqual(len(a), 4)

    def test_materias_1(self):
        a = AlumnoMateria.objects.filter(user=self.user)
        self.assertEqual(len(a), 4)
        materias_json = '['\
            '["6103", {"materia":"6103","estado":"A","creditos":8}],'\
            '["7540", {"materia":"7540","estado":"C","creditos":6}]]'
        self.client.cookies.load({'create_alumno': '1',
                                  'plancarrera': '{"id": 4}',
                                  'materias': materias_json})
        response = self.client.post(reverse('account_login'),
                                    {'login': self.user.username,
                                     'password': self.user.password},
                                    follow=True)

        self.assertEqual(len(response.redirect_chain), 2)
        self.assertEqual(response.redirect_chain,
                         [(reverse('home'), 302),
                          (reverse('facultad:home'), 302)])

        self.assertIsNone(response.cookies.get('create_alumno'))
        self.assertIsNone(response.cookies.get('plancarrera'))
        self.assertIsNone(response.cookies.get('materias'))

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0].level, MSG.SUCCESS)
        self.assertEqual(messages[0].message, _('Carrera agregada.'))
        self.assertEqual(messages[1].level, MSG.SUCCESS)
        self.assertEqual(messages[1].message, _('Se cargó 1 materia.'))

        a = AlumnoMateria.objects.filter(user=self.user)
        self.assertEqual(len(a), 5)

        m = a.get(materia__id=6103)
        self.assertEqual(m.state, 'A')

    def test_materias_varias(self):
        a = AlumnoMateria.objects.filter(user=self.user)
        self.assertEqual(len(a), 4)
        materias_json = '['\
            '["6103", {"materia":"6103","estado":"A","creditos":8}],'\
            '["6108", {"materia":"6108","estado":"F","creditos":8}],'\
            '["7540", {"materia":"7540","estado":"C","creditos":6}]]'
        self.client.cookies.load({'create_alumno': '1',
                                  'plancarrera': '{"id": 4}',
                                  'materias': materias_json})
        response = self.client.post(reverse('account_login'),
                                    {'login': self.user.username,
                                     'password': self.user.password},
                                    follow=True)

        self.assertEqual(len(response.redirect_chain), 2)
        self.assertEqual(response.redirect_chain,
                         [(reverse('home'), 302),
                          (reverse('facultad:home'), 302)])

        self.assertIsNone(response.cookies.get('create_alumno'))
        self.assertIsNone(response.cookies.get('plancarrera'))
        self.assertIsNone(response.cookies.get('materias'))

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0].level, MSG.SUCCESS)
        self.assertEqual(messages[0].message, _('Carrera agregada.'))
        self.assertEqual(messages[1].level, MSG.SUCCESS)
        self.assertEqual(messages[1].message, _('Se cargaron 2 materias.'))

        a = AlumnoMateria.objects.filter(user=self.user)
        self.assertEqual(len(a), 5)

        m = a.get(materia__id=6108)
        self.assertEqual(m.state, 'F')
        m = a.get(materia__id=6103)
        self.assertEqual(m.state, 'A')
        with self.assertRaises(ObjectDoesNotExist):
            a.get(materia__id=7540)
