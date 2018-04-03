# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from .models import User, UserProfile, user_signed_up_
from .forms import UserForm, UserProfileForm, UserDeleteForm


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = 'user'
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'

class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, _('Changes saved!'))
        return reverse('users:update')

    def get_object(self):
        try:
            profile = UserProfile.objects.get(user=self.request.user)
        except:
            profile = user_signed_up_(self.request, self.request.user, **self.kwargs)
        return profile

class UserAccountView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    delete_object = False
    delete_success_url = reverse_lazy('home')

    def get_success_url(self):
        return reverse('users:account')

    def get_object(self):
        return User.objects.get(username=self.request.user.username)

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super(UserAccountView, self).get_context_data(**kwargs)

        if not type(context['form']) is None:
            self.form_class = type(context['form'])

        if self.form_class is UserForm:
            context.setdefault('form_username', context['form'])
            context.setdefault('form_delete', UserDeleteForm)

        elif self.form_class is UserDeleteForm:
            context.setdefault('form_username', UserForm)
            if 'username' in context['form_username'].base_fields:
                context['form_username'].base_fields['username'].initial = self.object.username
            context.setdefault('form_delete', context['form'])

        del context['form']

        return context

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the delete success URL.
        """
        success_url = self.get_success_url()

        if self.delete_object:
            self.object = self.get_object()
            self.object.delete()
            success_url = self.delete_success_url
            messages.add_message(self.request, messages.SUCCESS, _('User deleted'))

        return HttpResponseRedirect(success_url)

    def post(self, request, *args, **kwargs):
        """
        Check whether form has been submitted for change username or delete
        user account.
        """
        if 'submit_delete' in request.POST:
            self.form_class = UserDeleteForm
            self.object = self.get_object()
            form = self.get_form()
            if form.is_valid():
                self.delete_object = True
                return self.delete(request, *args, **kwargs)
            else:
                self.get_context_data(**kwargs)
                return self.form_invalid(form)
        return super(UserAccountView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        """
        If the form is valid, set message and redirect to the supplied URL.
        """
        if type(form) == UserForm:
            messages.add_message(self.request, messages.SUCCESS, _('Username changed'))
        return super(UserAccountView, self).form_valid(form)
