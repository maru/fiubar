# -*- coding: utf-8 -*-
from django import forms
from captcha.fields import ReCaptchaField


class SignupForm(forms.Form):
    """
    Signup form with recaptcha field.
    """
    captcha = ReCaptchaField()

    field_order = ['username', 'email', 'password1',  'captcha',]


    def signup(self, request, user):
        """ Required, or else it throws deprecation warnings """
        pass
