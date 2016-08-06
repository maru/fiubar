# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .models import User, UserProfile
from .forms import UserProfileForm


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = 'user'
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        if hasattr(context['user'], 'profile'):
            p = context['user'].profile
            p.status = []
            if p.student:
                p.status.append(_('Student'))
            if p.professor:
                p.status.append(_('Professor'))
            if p.assistant:
                p.status.append(_('Assistant'))
            if p.professional:
                p.status.append(_('Professional'))
            p.status = ', '.join(p.status)
            context['profile'] = p
        return context

class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):

    fields = ['username', ]
    template_name = 'users/userprofile_form.html'
    model = User
    # form_class = UserProfileForm

    # def get_initial(self):
    #     user = self.request.user
    #     return { 'user' : user,
    #              'username': user.username }

    # send the user back to their own page after a successful update
    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, _('Changes saved!'))
        # return reverse('users:update')
        url = reverse('users:detail',
                       kwargs={'username': self.request.user.username})
        print(url)
        return url

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)

    # def post(self, request, *args, **kwargs):
    #     form = self.get_form()
    #     if form.is_valid():
    #         user = User.objects.get(username=self.request.user.username)
    #         user.username = form.cleaned_data['username']
    #         user.save()
    #         return super(UserUpdateView, self).post(request, *args, **kwargs)
    #     # else
    #     self.object = self.get_object()
    #     return self.render_to_response(self.get_context_data())
from .utils import generate_avatar

def show_avatar(request, username):
    user =  get_object_or_404(User, username=username)
    content = generate_avatar(user.username[0], user.email)
    response = HttpResponse(content_type='image/png')
    response['Content-Length'] = len(content)
    response.write(content)
    return response
