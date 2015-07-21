# -*- coding: utf-8 -*-
"""
Copyright (c) 2007, James Bennett
Copyright (c) 2008, OpenMate - Some changes introduced

Form and validation code for user registration.

"""


import re

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.conf import settings

PASSWORD_REGEXP = getattr(settings, 'PASSWORD_REGEXP', r'^.{6,}.*$')
password_re = re.compile(PASSWORD_REGEXP)
HELP_TEXT_PASSWORD = getattr(settings, 'HELP_TEXT_PASSWORD', _(u'Your password must have at least 6 characters.'))

class PasswordResetForm(forms.Form):
    email = forms.EmailField(max_length=200)

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        try:
            self.user = User.objects.get(email__iexact=email)
        except:
            raise forms.ValidationError(_("That e-mail address doesn't have an associated user account. Are you sure you've registered?"))
        return email

class PasswordChangeForm(forms.Form):
    new_password1 = forms.CharField(widget=forms.PasswordInput(), label=_('Password'),
                    help_text=_(HELP_TEXT_PASSWORD))
    new_password2 = forms.CharField(widget=forms.PasswordInput(), label=_('Password (again, to catch typos)'),
                    help_text=_(u'Re-enter your password to verify.'))

    def clean_password(self):
        """
        Validates that the password matches the required characters and
        length.

        """
        if not password_re.search(self.cleaned_data['new_password1']):
            raise forms.ValidationError(_(u'Password not valid.'))
        return self.cleaned_data['new_password1']

    def clean_password_verify(self):
        """
        Validates that the two password inputs match.

        """
        if 'new_password1' in self.cleaned_data and 'new_password2' in self.cleaned_data and \
           self.cleaned_data['new_password1'] == self.cleaned_data['new_password2']:
            return self.cleaned_data['new_password2']
        raise forms.ValidationError(_('You must type the same password each time'))

