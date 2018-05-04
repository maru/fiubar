from django.urls import reverse
from django.utils.translation import ugettext as _
from test_plus.test import TestCase

from ..models import UserProfile


class TestUser(TestCase):

    def setUp(self):
        self.user = self.make_user()

    def test__str__(self):
        self.assertEqual(
            self.user.__str__(),
            'testuser'  # This is the default username for self.make_user()
        )

    def test_get_absolute_url(self):
        self.assertEqual(
            self.user.get_absolute_url(),
            '/users/testuser/'
        )


class TestUserProfile(TestCase):

    def setUp(self):
        self.user = self.make_user()
        self.profile = UserProfile.objects.get(user=self.user)

    def test__str__(self):
        self.assertEqual(
            self.profile.__str__(),
            self.user.username
        )

    def test_get_absolute_url(self):
        self.assertEqual(self.profile.get_absolute_url(),
                         reverse('users:detail',
                                 kwargs={'username': self.user.username}))

    def test_get_status(self):
        self.profile.professional = True
        self.profile.professor = True
        self.profile.assistant = True
        self.profile.student = True

        s = []
        s.append(str(_('Professional')))
        s.append(str(_('Professor')))
        s.append(str(_('Assistant')))
        s.append(str(_('Student')))
        self.assertEqual(self.profile.status, ', '.join(s))
