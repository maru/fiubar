from django.test import RequestFactory
from test_plus.test import TestCase

from .forms import SignupForm


class SignupFormTestCase(TestCase):

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
