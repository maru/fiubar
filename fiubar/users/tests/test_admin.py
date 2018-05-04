from django import forms
from django.contrib import admin
from test_plus.test import TestCase

from ..admin import MyUserCreationForm, UserProfileAdmin
from ..models import UserProfile


class TestMyUserCreationForm(TestCase):

    def setUp(self):
        self.user = self.make_user()

    def test_clean_username_success(self):
        # Instantiate the form with a new username
        form = MyUserCreationForm({
            'username': 'alamode',
            'password1': 'ghfjdksl',
            'password2': 'ghfjdksl',
        })
        # Run is_valid() to trigger the validation
        valid = form.is_valid()
        self.assertTrue(valid)

        # Run the actual clean_username method
        username = form.clean_username()
        self.assertEqual('alamode', username)

    def test_clean_username_false(self):
        # Instantiate the form with the same username as self.user
        form = MyUserCreationForm({
            'username': self.user.username,
            'password1': 'ghfjdksl',
            'password2': 'ghfjdksl',
        })
        # Run is_valid() to trigger the validation, which is going to fail
        # because the username is already taken
        valid = form.is_valid()
        self.assertFalse(valid)

        # The form.errors dict should contain a single error called 'username'
        self.assertTrue(len(form.errors) == 1)
        self.assertTrue('username' in form.errors)


class TestUserProfileAdmin(TestCase):

    def test_form_field(self):
        model = UserProfile
        ma = UserProfileAdmin(model, admin.site)
        ff = ma.formfield_for_dbfield(model._meta.get_field('name'),
                                      request=None)

        widget = ff.widget
        self.assertIsInstance(widget, forms.TextInput)

    def test_form_field_bio(self):
        model = UserProfile
        ma = UserProfileAdmin(model, admin.site)
        ff = ma.formfield_for_dbfield(model._meta.get_field('bio'),
                                      request=None)

        widget = ff.widget
        self.assertIsInstance(widget, forms.Textarea)
        self.assertTrue(widget.attrs['class'], 'vURLField')
        self.assertTrue(widget.attrs['rows'], '4')
