# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _

from .models import User, UserProfile


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserCreationForm(UserCreationForm):

    error_message = UserCreationForm.error_messages.update({
        'duplicate_username': 'This username has already been taken.'
    })

    class Meta(UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])


@admin.register(User)
class MyUserAdmin(AuthUserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    fieldsets = (
        ('User Profile', {'fields': ()}),
    ) + AuthUserAdmin.fieldsets
    list_display = ('username', 'email', 'is_active',
                    'is_staff', 'is_superuser')
    search_fields = ['username', 'email']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    # form = MyUserChangeForm
    # add_form = MyUserCreationForm
    fieldsets = ((None, {'fields': ('user', 'name', 'avatar', 'location',
                                    'website', 'bio')}),
                 (_('Status'), {'fields': ('student', 'assistant',
                                           'professional', 'professor')}))
    list_display = ['user', 'name', 'bio']
    search_fields = ['user', 'name', 'bio']

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(UserProfileAdmin, self).\
            formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'bio':
            formfield.widget.attrs.update({'class': 'vURLField', 'rows': '4'})
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield
