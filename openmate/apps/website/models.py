# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import Group
from django.contrib import admin

""" Based in django-navbar component """
USER_TYPE_CHOICES = [
	('A', _('Anonymous')),
	('U', _('User')),
	('S', _('Staff')),
	('X', _('Superuser')),
	('N', _('Not logged in')), # Only when user is Anonymous
]

class MenuEntryManager(models.Manager):
	def get_menu_entries(self, user):
		list_entries = self.filter(is_active=True).order_by('order')
		if not user.is_superuser:
			list_entries = list_entries.exclude(user_type='X')
		if not user.is_staff:
			list_entries = list_entries.exclude(user_type='S')
		if not user.is_authenticated():
			list_entries = list_entries.exclude(user_type='U')
		else:
			list_entries = list_entries.exclude(user_type='N')
		return list_entries

class MenuEntry(models.Model):
	name   = models.CharField(max_length=50, unique=True,
							  help_text='text seen in the menu')
	title  = models.CharField(max_length=50, blank=True,
							  help_text='mouse hover description')
	url	= models.CharField(max_length=200, unique=True)
	order  = models.IntegerField(default=0, unique=True)
	user_type = models.CharField('user login type', max_length=1,
								 choices=USER_TYPE_CHOICES,
								 default=USER_TYPE_CHOICES[0])
	groups	= models.ManyToManyField(Group, null=True, blank=True)
	is_active = models.BooleanField(default=True)

	objects = MenuEntryManager()

	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ['order']
		verbose_name_plural = 'Menu Entries'

class MenuEntryAdmin(admin.ModelAdmin):
	list_display = ('name', 'title', 'url', 'user_type')
	search_fields = ('name', 'title', 'url')

admin.site.register(MenuEntry)

"""
from django.contrib.sites.models import Site
class MetaContent(models.Model):
	site = models.ForeignKey(Site)
	name = models.CharField(_('meta name'), max_length=20)
	content = models.CharField(_('meta content'), max_length=250)
	http_equiv = models.BooleanField(_('meta http-equiv'))
	# objects = WebsiteManager()

	class Meta:
		db_table = 'website_metacontent'
		verbose_name = _('website meta tag')
		verbose_name_plural = _('website meta tags')
		ordering = ('site', 'name')

	def __unicode__(self):
		return '%s %s' % (self.site, self.name)
"""
