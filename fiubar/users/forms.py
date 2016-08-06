# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

from .models import User, UserProfile

class UserProfileForm(forms.ModelForm):
    username = forms.CharField(
        max_length = 30,
    )
    avatar = forms.ImageField(required=False)
    name = forms.CharField(required=False, max_length=255)
    location = forms.CharField(required=False, max_length=255)
    website = forms.CharField(required=False, max_length=255)
    bio = forms.CharField(
        required = False,
        widget = forms.Textarea(),
    )

    helper = FormHelper()
    helper.form_class = 'users-update'
    helper.form_action = 'users:update'
    helper.layout = Layout(
        'username',
        HTML('{% if form.avatar.value %}<img class="img-responsive" src="{{ MEDIA_URL }}{{ form.avatar.value }}">{% endif %}', ),
        'avatar',
        'name',
        'location',
        'website',
        HTML('{% load i18n %}<label for="id_status" class="control-label ">{% trans "Status" %}</label>'),
        Div('student', 'assistant', 'professional', 'professor', css_class='users-update-status'),
        Field('bio', rows="3", css_class='input-xlarge'),
        FormActions(
            Submit('submit', _('Save changes'), css_class="btn-primary"),
        ),
    )

    def xclean(self):
        self.cleaned_data.update({'user': self.initial['user']})
        return self.cleaned_data

    def clean_username(self):
        """
        Check if username already exists.
        """
        try:
            if self.initial['username'] != self.cleaned_data['username']:
                user = User.objects.get(username=self.cleaned_data['username'])
                raise ValidationError(_('A user with that username already exists.'))
        except User.DoesNotExist:
            pass
        return self.cleaned_data['username']

    def save(self, commit=True):
        # self.data[]
        # 'location':
        # 'website':
        # 'bio':
        # 'status': ['student', 'professional'],
        # 'name':
        # 'username':
        # self.files['avatar']
        print('save')
        #print(type(self.instance), dir(self.instance))
        #'self.instance.username = self.cleaned_data['username']
        return super(UserProfileForm, self).save(commit)


    class Meta:
        model = UserProfile
        exclude = [ 'user' ]
