from django.contrib.messages import constants as MSG
from django.core.exceptions import ObjectDoesNotExist
from django.test import RequestFactory
from django.urls import reverse
from django.utils.translation import ugettext as _
from test_plus.test import TestCase

from ..forms import DELETE_CONFIRMATION_PHRASE, UserDeleteForm, UserForm
from ..models import User, UserProfile
from ..views import UserAccountView, UserRedirectView


class BaseUserTestCase(TestCase):

    def setUp(self):
        self.user = self.make_user()
        self.factory = RequestFactory()


class TestUserRedirectView(BaseUserTestCase):

    def test_get_redirect_url(self):
        # Instantiate the view directly. Never do this outside a test!
        view = UserRedirectView()
        # Generate a fake request
        request = self.factory.get('/fake-url')
        # Attach the user to the request
        request.user = self.user
        # Attach the request to the view
        view.request = request
        # Expect: '/users/testuser/', as that is the default username for
        #   self.make_user()
        self.assertEqual(
            view.get_redirect_url(),
            '/users/testuser/'
        )


class TestProfileUpdateView(BaseUserTestCase):

    def test_get_success_url(self):
        self.client.force_login(self.user)
        assert self.user.is_authenticated

        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.name, "")

        response = self.client.post(
            reverse('users:update'),
            {'bio': 'The Catcher in the Rye', 'name': 'J.D. Salinger'},
            follow=True)

        self.assertEqual(response.status_code, 200)

        expected = _("Changes saved!")
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].level, MSG.INFO)
        self.assertEqual(messages[0].message, expected)

        profile.refresh_from_db()
        self.assertEqual(profile.name, 'J.D. Salinger')

    def test_profile_does_not_exist(self):
        self.client.force_login(self.user)
        assert self.user.is_authenticated

        # Delete profile
        profile = UserProfile.objects.get(user=self.user)
        profile.delete()

        with self.assertRaises(ObjectDoesNotExist):
            UserProfile.objects.get(user=self.user)

        response = self.client.get(reverse('users:update'))

        self.assertEqual(response.status_code, 200)

        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.name, '')


class TestUserAccountView(BaseUserTestCase):

    def setUp(self):
        # call BaseUserTestCase.setUp()
        super(TestUserAccountView, self).setUp()
        # Instantiate the view directly. Never do this outside a test!
        self.view = UserAccountView()
        # Generate a fake request
        request = self.factory.get('/fake-url')
        # Attach the user to the request
        request.user = self.user
        # Attach the request to the view
        self.view.request = request

    def test_get_success_url(self):
        # Expect: '/users/testuser/', as that is the default username for
        #   self.make_user()
        self.assertEqual(
            self.view.get_success_url(),
            '/users/~account/'
        )

    def test_get_object(self):
        # Expect: self.user, as that is the request's user object
        self.assertEqual(
            self.view.get_object(),
            self.user
        )

    def test_delete(self):
        self.client.force_login(self.user)
        assert self.user.is_authenticated

        self.user.set_password('password')

        response = self.client.post(
            reverse('users:account'),
            {'sudo_login': self.user.username,
             'confirmation_phrase': str(DELETE_CONFIRMATION_PHRASE),
             'sudo_password': 'password',
             'submit_delete': 'Delete my account'},
            follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0], ('/', 302))

        expected = _("User deleted")
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].level, MSG.SUCCESS)
        self.assertEqual(messages[0].message, expected)

        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(username=self.user.username)

    def test_delete_bad(self):
        self.client.force_login(self.user)
        assert self.user.is_authenticated

        response = self.client.post(
            reverse('users:account'),
            {'sudo_login': self.user.username,
             'confirmation_phrase': 'bad confirmation phrase',
             'sudo_password': 'password',
             'submit_delete': 'Delete my account'},
            follow=True)

        self.assertEqual(response.status_code, 200)

        form_delete = response.context['form_delete']
        self.assertIsInstance(form_delete, UserDeleteForm)
        self.assertEqual(len(form_delete.errors), 1)
        self.assertTrue(form_delete.has_error('confirmation_phrase'))

        form_username = response.context['form_username']
        self.assertNotIsInstance(form_username, UserForm)

        User.objects.get(username=self.user.username)

    def test_post_empty(self):
        self.client.force_login(self.user)
        assert self.user.is_authenticated

        response = self.client.post(
            reverse('users:account')
        )

        self.assertEqual(response.status_code, 200)

        form_delete = response.context['form_delete']
        self.assertNotIsInstance(form_delete, UserDeleteForm)

        form_username = response.context['form_username']
        self.assertTrue(isinstance(form_username, UserForm))
        self.assertEqual(len(form_username.errors), 1)
        self.assertTrue(form_username.has_error('username'))

    def test_change_username(self):
        self.client.force_login(self.user)
        assert self.user.is_authenticated

        response = self.client.post(
            reverse('users:account'),
            {'username': 'newusername'},
            follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0],
                         (reverse('users:account'), 302))

        expected = _('Username changed')
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].level, MSG.SUCCESS)
        self.assertEqual(messages[0].message, expected)

        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(username=self.user.username)
