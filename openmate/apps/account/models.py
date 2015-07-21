# -*- coding: utf-8 -*-
"""
Copyright (c) 2007, James Bennett
Copyright (c) 2008, OpenMate - Some changes introduced

A registration profile model and associated manager.

The ``RegistrationProfile`` model and especially its custom manager
implement nearly all the logic needed to handle user registration and
account activation, so before implementing something in a view or
form, check here to see if they can take care of it for you.

Also, be sure to see the note on ``RegistrationProfile`` about use of the
``AUTH_PROFILE_MODULE`` setting.

"""


import datetime, random, re, sha

from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, SiteProfileNotAvailable
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.contrib import admin

SHA1_RE = re.compile('^[a-f0-9]{40}$')

class PasswordResetManager(models.Manager):
    def create_key(self, user):
        salt = sha.new(str(random.random())).hexdigest()[:5]
        pwdreset_key = sha.new(salt+user.username).hexdigest()
        return self.create(user=user, pwdreset_key=pwdreset_key)

    def is_valid(self, pwdreset_key):
        if SHA1_RE.search(pwdreset_key):
            try:
                pwdreset = self.get(pwdreset_key=pwdreset_key)
            except self.model.DoesNotExist:
                return False
            if not pwdreset.is_expired:
                # Account exists and has a non-expired key. Expire it.
                user = pwdreset.user
                user.is_expired = True
                user.save()
                return user
        return False

    def expire_key(self, pwdreset_key):
        try:
            pwdreset = self.get(pwdreset_key=pwdreset_key)
        except self.model.DoesNotExist:
            return False
        pwdreset.is_expired = True
        pwdreset.save()
        
        
       
class PasswordReset(models.Model):
    """
    Password reset keys.
    """
    user = models.ForeignKey(User, verbose_name=_('user'))
    pwdreset_key = models.CharField(_('password reset key'), max_length=40)
    date_key = models.DateTimeField(default=datetime.datetime.now())
    is_expired = models.BooleanField(default=False)
    
    objects = PasswordResetManager()
    
    class Meta:
        verbose_name = _('password reset key')
        verbose_name_plural = _('password reset keys')
    
    class Admin(admin.ModelAdmin):
        list_display = ('__unicode__', 'pwdreset_key', 'date_key', 'is_expired')
        search_fields = ('user__username', 'user__first_name')

    def __unicode__(self):
        return _('Password reset for %(username)s') % {'username' : self.user.username}

   
    def send_mail(self, email_template_name):
        current_site = Site.objects.get_current()
        site_name = current_site.name
        domain = current_site.domain
        c = {
            'pwdreset_key': self.pwdreset_key,
            'email': self.user.email,
            'domain': domain,
            'site_name': site_name,
            'user': self.user,
        }
        message = render_to_string(email_template_name, c)
        r = send_mail(_('Password reset on %s') % site_name, message, None, [self.user.email])
        return r

admin.site.register(PasswordReset, PasswordReset.Admin)
class UserSessionManager(models.Manager):
    def get_user_last_login(self, user):
        try:
            return self.filter(user=user).order_by('-last_login')[1].last_login
        except:
            return None
        
class UserSession(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'))
    last_login = models.DateTimeField(default=datetime.datetime.now())
    ip_address = models.IPAddressField()

    objects = UserSessionManager()
    
    class Meta:
        verbose_name = _('user session')
        verbose_name_plural = _('user sessions')
    
    class Admin(admin.ModelAdmin):
        list_display = ('user', 'last_login', 'ip_address')
        search_fields = ('user__username', 'user__first_name')
        date_hierarchy = 'last_login'

    def __unicode__(self):
        return _('Last login for user %s') % self.user

admin.site.register(UserSession, UserSession.Admin)
