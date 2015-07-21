# -*- coding: utf-8 -*-
"""
Copyright (c) 2007, James Bennett
Copyright (c) 2008, OpenMate - Some changes introduced

Views which allow users to create and activate accounts.

"""

from django.utils.translation import ugettext as _
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from openmate.core.log import logger

from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.contrib.auth import views as auth_views
from account.forms import PasswordResetForm, PasswordChangeForm
from account.models import PasswordReset, UserSession
from django.contrib.auth.models import User

import re
email_re = re.compile('[^@]+@[^@]+')
def login(request, template_name):
    if (request.method == 'POST'):
        # Default error_message
        error_message = "Password not valid"
        try:
            username = request.POST.get('username', '').strip()
            # Check if user entered email to login
            if email_re.search(username):
                # "username" is an email. Get his/her username.
                user = User.objects.get(email=username)
            else:
                # Get real username in case user entered ignore-case username
                user = User.objects.get(username__iexact=username)

            post_copy = request.POST.copy()
            post_copy['username'] = user.username
            request.POST = post_copy
        except User.DoesNotExist:
            error_message = "Username doesn't exist"
        response = auth_views.login(request, template_name)
        ip_address = request.META.get('REMOTE_ADDR')
        if (type(response) == HttpResponseRedirect):
            UserSession.objects.create(user=user, ip_address=ip_address)
            logger.info("%s - account-login: user '%s'" % (ip_address, username))
        else:
            logger.error("%s - account-login: user '%s', error: '%s'" % (ip_address, username, error_message))
    else:
        response = auth_views.login(request, template_name)
    return response


def password_reset(request, template_name, email_template_name):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            "Generates a key and sends it to the user"
            from django.core.mail import send_mail
            pwdreset_key = PasswordReset.objects.create_key(form.user)
            pwdreset_key.send_mail(email_template_name)
            logger.info("%s - account-password_reset: email '%s'" % (request.META.get('REMOTE_ADDR'), form.user.email))
            return HttpResponseRedirect('%sdone/' % request.path)
        else:
            logger.error("%s - account-password_reset: email '%s' not found" % (request.META.get('REMOTE_ADDR'), form.data['email']))
    else:
        form = PasswordResetForm()
    return render_to_response(template_name, {'form': form },
                              context_instance=RequestContext(request))

def password_change(request, pwdreset_key):
    user = PasswordReset.objects.is_valid(pwdreset_key)
    if not user:
        logger.error("%s - account-pwdchange: key '%s', error: '%s'" % (request.META.get('REMOTE_ADDR'), pwdreset_key, 'Key not found'))
        return render_to_response('account/password_change_form.html', context_instance=RequestContext(request))
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['new_password1'])
            user.save()
            PasswordReset.objects.expire_key(pwdreset_key)
            logger.info("%s - account-pwdchange: key '%s', user '%s'" % (request.META.get('REMOTE_ADDR'), pwdreset_key, user.username))
            return render_to_response('account/password_change_done.html', context_instance=RequestContext(request))
        else:
            logger.error("%s - account-pwdchange: key '%s', user '%s', error: '%s'" % (request.META.get('REMOTE_ADDR'), pwdreset_key, user.username, 'Password not valid'))
    else:
        form = PasswordChangeForm()
    return render_to_response('account/password_change_form.html', { 'form' : form, 'user_cache' : user },
                              context_instance=RequestContext(request))

from django.core.urlresolvers import reverse
def home(request):
    if request.user.is_authenticated():
        try:
            return HttpResponseRedirect(reverse('profile-show'))
        except Exception, e:
            return HttpResponseRedirect(reverse('account-password_change_form'))
    else:
		return HttpResponseRedirect(reverse('account-login'))
