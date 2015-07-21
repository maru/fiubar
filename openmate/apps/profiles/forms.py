# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _
from openmate.core.widgets import SelectDateWidget
from profiles.models import Profile, ServiceInstantMessenger, ServiceSocialNetwork, LinkSocialNetwork, LinkInstantMessenger, LinkWebsite
from openmate.core import image
from datetime import datetime

class ProfileForm(forms.Form):
    """Form for editing profile."""
    username = forms.CharField(widget=forms.HiddenInput())
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(maxlength=200)))
    gender = forms.CharField(widget=forms.RadioSelect(choices=Profile.GENDER_CHOICES), required=False)
    nickname = forms.CharField(max_length=30, required=False)
    birthdate = forms.DateField(widget=SelectDateWidget(years=range(datetime.now().year, 1900, -1)), required=False)
    location = forms.CharField(max_length=100, widget=forms.TextInput(), required=False)
    interests = forms.CharField(required=False)

    def save(self, profile):
        # Updates user's email
        if profile.user.email != self.cleaned_data['email']:
            profile.user.email = self.cleaned_data['email']
            profile.user.save()
        # Updates profile data
        profile.gender = self.cleaned_data['gender']
        profile.nickname = self.cleaned_data['nickname']
        profile.birthdate = self.cleaned_data['birthdate']
        profile.location = self.cleaned_data['location']
        profile.interests = self.cleaned_data['interests']
        profile.save()

class UploadPhotoForm(forms.Form):
    """Form for uploading profile photo."""
    avatar = forms.ImageField()  
   
class LinkSocialNetworkForm(forms.Form):
    form_name = forms.CharField(widget=forms.HiddenInput(), initial='sn_form')
    network = forms.ChoiceField(choices=ServiceSocialNetwork.objects.choices())
    account = forms.CharField(max_length=200)

    def save(self, user):
        slug = self.cleaned_data['network']
        account = self.cleaned_data['account']
        network = ServiceSocialNetwork.objects.get(slug=slug)
        LinkSocialNetwork.objects.create(user=user, service=network, account=account)
        
class LinkInstantMessengerForm(forms.Form):
    form_name = forms.CharField(widget=forms.HiddenInput(), initial='im_form')
    messenger = forms.ChoiceField(choices=ServiceInstantMessenger.objects.choices())
    account = forms.CharField(max_length=200)

    def save(self, user):
        slug = self.cleaned_data['messenger']
        account = self.cleaned_data['account']
        messenger = ServiceInstantMessenger.objects.get(slug=slug)
        LinkInstantMessenger.objects.create(user=user, service=messenger, account=account)

class LinkWebsiteForm(forms.Form):
    form_name = forms.CharField(widget=forms.HiddenInput(), initial='w_form')
    name = forms.CharField(max_length=50)
    url = forms.URLField(max_length=250)

    def save(self, user):
        name = self.cleaned_data['name']
        url = self.cleaned_data['url']
        LinkWebsite.objects.create(user=user, name=name, url=url)
