from django.test import RequestFactory
from test_plus.test import TestCase

from .forms import SignupForm


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
        self.user = self.make_user()

    def test_home_page(self):
        self.client.force_login(self.user)
        assert self.user.is_authenticated

        response = self.client.get('/', follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain,
                         [('/facultad/', 302)])

        self.assertTemplateUsed(response, 'facultad/home.html')
