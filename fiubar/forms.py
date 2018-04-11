# -*- coding: utf-8 -*-
from captcha.fields import ReCaptchaField
from django import forms
from django.conf import settings


class SignupForm(forms.Form):
    """
    Signup form with recaptcha field.
    """
    field_order = ['username', 'email', 'password1', ]

    if hasattr(settings, 'RECAPTCHA_PUBLIC_KEY'):
        captcha = ReCaptchaField()
        field_order.append('captcha')

    def signup(self, request, user):
        """ Required, or else it throws deprecation warnings """
        pass
