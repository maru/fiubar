# -*- coding: utf-8 -*-
from allauth.account.signals import user_signed_up
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from .utils import generate_avatar


@python_2_unicode_compatible
class User(AbstractUser):
    pass

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='profile')
    name = models.CharField(_('Name'), blank=True, max_length=255)
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


# @receiver(user_signed_up, dispatch_uid="create_profile_when_user_signed_up")
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile.objects.get_or_create(user=instance)[0]
        profile.avatar = generate_avatar(instance.username[0], instance.email)
        profile.save()
        return profile
