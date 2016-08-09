# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class User(AbstractUser):
    pass

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='profile')
    name = models.CharField(_('Name'), blank=True, max_length=255)
    # TODO
    # avatar = models.ImageField(_('Avatar'), upload_to='avatars/users/',
    #                            null=True, blank=True, max_length=255)
    avatar = models.CharField(_('Picture'), blank=True, max_length=255)
    location = models.CharField(_('Location'), blank=True, max_length=255)
    website = models.URLField(_('Website'), blank=True, max_length=255)
    student = models.BooleanField(_('Student'), default=False)
    professor = models.BooleanField(_('Professor'), default=False)
    assistant = models.BooleanField(_('Assistant'), default=False)
    professional = models.BooleanField(_('Professional'), default=False)
    bio = models.CharField(_('About me'), blank=True, max_length=160)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.user.username})

    def _get_status(self):
        s = []
        if self.professional:
            s.append(str(_('Professional')))
        if self.professor:
            s.append(str(_('Professor')))
        if self.assistant:
            s.append(str(_('Assistant')))
        if self.student:
            s.append(str(_('Student')))
        return ', '.join(s)
    status = property(_get_status)

    class Meta:
        verbose_name = _("profile")

from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from .utils import generate_avatar

@receiver(user_signed_up, dispatch_uid="create_profile_when_user_signed_up")
def user_signed_up_(request, user, **kwargs):
    profile = UserProfile.objects.get_or_create(user=user)[0]
    profile.avatar = generate_avatar(user.username[0], user.email)
    profile.save()
    return profile
