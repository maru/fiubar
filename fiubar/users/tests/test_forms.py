from test_plus.test import TestCase

from ..forms import DELETE_CONFIRMATION_PHRASE, UserDeleteForm, UserForm


class BaseUserTestCase(TestCase):

    def setUp(self):
        self.user = self.make_user()


class TestUserForm(BaseUserTestCase):

    def test_same_username(self):
        form = UserForm(initial={'username': self.user.username},
                        data={'username': self.user.username})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error('username'))

    def test_repeated_username(self):
        user2 = self.make_user('testuser2')

        form = UserForm(initial={'username': self.user.username},
                        data={'username': user2.username})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error('username'))


class TestUserDeleteForm(BaseUserTestCase):

    def test_bad_login(self):
        self.user.set_password('password')

        form = UserDeleteForm(
            data={'sudo_login': 'bad_username',
                  'confirmation_phrase': str(DELETE_CONFIRMATION_PHRASE),
                  'sudo_password': 'password',
                  'submit_delete': 'Delete my account'})
        form.instance = self.user

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error('sudo_login'))

    def test_bad_password(self):
        form = UserDeleteForm(
            data={'sudo_login': self.user.username,
                  'confirmation_phrase': str(DELETE_CONFIRMATION_PHRASE),
                  'sudo_password': 'bad_password',
                  'submit_delete': 'Delete my account'})
        form.instance = self.user

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error('sudo_password'))
