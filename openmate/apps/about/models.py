# -*- coding: utf-8 -*-
"""
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.db import models

class Bug(models.Model):
    user        = models.ForeignKey(User, null=True)
    date        = models.DateTimeField(auto_now_add=True)
    subject     = models.CharField(max_length=100)
    description = models.TextField()
    solved      = models.BooleanField(default=False)
    notes       = models.TextField(null=True)

    class Admin:
        list_display = ('subject', 'user', 'date', 'description', 'solved', 'notes')
        list_filter = ('user', 'solved')
        list_per_page = 20
        search_fields = ['subject', 'description', 'notes', ]


class Idea(models.Model):
    STATES = (
        ('N', _('New')),
        ('W', _('Working')),
        ('D', _('Implemented')),
    )
    IDEAS_CATEGORIES = (
        (0, _('Materias')),
        (1, _('Grupos')),
        (2, _('Perfil')),
        (3, _('Noticias')),
        (5, _('Encuestas')),
        (4, _('General')),
    )
    user        = models.ForeignKey(User)
    date        = models.DateTimeField(auto_now_add=True)
    subject     = models.CharField(max_length=100)
    description = models.TextField()
    category    = models.IntegerField(choices=IDEAS_CATEGORIES)
    state       = models.CharField(max_length=1, choices=STATES, default='N')
    positive_votes = models.IntegerField(default=0)
    negative_votes = models.IntegerField(default=0)
    notes       = models.TextField(null=True)

    class Admin:
        list_display = ('subject', 'user', 'date', 'category', 'description', 'state', 'notes')
        list_filter = ('user', 'state', 'category', )
        list_per_page = 20
        search_fields = ['subject', 'description', 'notes', ]

"""
