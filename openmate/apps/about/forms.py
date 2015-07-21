# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _
from about.models import Bug, Idea

class BugsForm(forms.Form):
    subject     = forms.CharField(max_length=100, label=_(u'Subject'))
    description = forms.CharField(widget=forms.Textarea, label=_(u'Description'))

class IdeasForm(forms.Form):
    category    = forms.ChoiceField(choices=Idea.IDEAS_CATEGORIES, label=_(u'Category'))
    subject     = forms.CharField(max_length=100, label=_(u'Asunto'))
    description = forms.CharField(widget=forms.Textarea, label=_(u'Description'))

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label=_(u'Tu nombre:'))
    email = forms.EmailField(label=_(u'Tu email:'))
    description = forms.CharField(widget=forms.Textarea, label=_(u'Description'))
