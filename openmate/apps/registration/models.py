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


from django.contrib.auth.models import User, SiteProfileNotAvailable
from django.utils.translation import ugettext_lazy as _
#from django.contrib import admin
from django.db import models
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import datetime, random, sha, re

SHA1_RE = re.compile('^[a-f0-9]{40}$')


class RegistrationManager(models.Manager):
	"""
	Custom manager for the ``RegistrationProfile`` model.

	The methods defined here provide shortcuts for account creation
	and activation (including generation and emailing of activation
	keys), and for cleaning out expired inactive accounts.

	"""
	def activate_user(self, activation_key):
		"""
		Validates an activation key and activates the corresponding
		``User`` if valid.

		If the key is valid and has not expired, returns the ``User``
		after activating.

		If the key is not valid or has expired, returns ``False``.

		If the key is valid but the ``User`` is already active,
		returns the ``User``.

		"""
		# Make sure the key we're trying conforms to the pattern of a
		# SHA1 hash; if it doesn't, no point even trying to look it up
		# in the DB.
		if SHA1_RE.search(activation_key):
			try:
				profile = self.get(activation_key=activation_key)
			except self.model.DoesNotExist:
				# Activation key doesn't exist
				return False
			user = profile.user
			if not profile.activation_key_expired() and not user.is_active:
				# Account exists and has a non-expired key. Activate it.
				user.is_active = True
				user.save()
				try:
					self.create_user_profile(user)
				except SiteProfileNotAvailable:
					pass
				return user
		return False

	def create_user_profile(self, user):
		"""
		Creates site-specific profile for this user. Raises
		SiteProfileNotAvailable if this site does not allow profiles.
		"""
		if not getattr(settings, 'AUTH_PROFILE_MODULE', None):
			raise SiteProfileNotAvailable
		try:
			app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
			profile_model = models.get_model(app_label, model_name)
			profile_model.objects.create_profile(user=user)
		except (ImportError, ImproperlyConfigured):
			raise SiteProfileNotAvailable

	def create_inactive_user(self, username, password, first_name, last_name,
							 email, send_email=True, profile_callback=None):
		"""
		Creates a new, inactive ``User``, generates a
		``RegistrationProfile`` and emails its activation key to the
		``User``. Returns the new ``User``.

		To disable the email, call with ``send_email=False``.

		To enable creation of a custom user profile along with the
		``User`` (e.g., the model specified in the
		``AUTH_PROFILE_MODULE`` setting), define a function which
		knows how to create and save an instance of that model with
		appropriate default values, and pass it as the keyword
		argument ``profile_callback``. This function should accept one
		keyword argument:

		``user``
			The ``User`` to relate the profile to.

		"""
		# Creates the user
		new_user = User.objects.create_user(username, email, password)
		new_user.is_active = False
		new_user.first_name = first_name
		new_user.last_name = last_name
		new_user.save()

		# And finally create the registration profile.
		registration_profile = self.create_profile(new_user)

		# Create site-specific profile, if specified.
		if profile_callback is not None:
			profile_callback(new_user)

		if send_email:
			from django.template.loader import render_to_string
			from django.contrib.sites.models import Site
			from django.core.mail import send_mail

			current_site = Site.objects.get_current()
			subject = _('Activate your new account at %(current_name)s') \
							  % {'current_name' : current_site.name }
			message = render_to_string('registration/activation_email.html',
						  { 'activation_key': registration_profile.activation_key,
							'expiration_days': getattr(settings, 'ACCOUNT_ACTIVATION_DAYS', 5),
							'site_url': 'http://%s/' % current_site.domain,
							'site_name': current_site.name,
						  })
			send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [new_user.email])

		return new_user

	def create_profile(self, user):
		"""
		Given a ``User``, creates, saves and returns a
		``RegistrationProfile`` for that ``User``, generating the
		activation key from a combination of the ``User``'s username
		and a random salt.

		"""
		salt = sha.new(str(random.random())).hexdigest()[:5]
		activation_key = sha.new(salt+user.username).hexdigest()
		return self.create(user=user,
						   activation_key=activation_key)

	def delete_expired_users(self):
		"""
		Removes expired instances of ``RegistrationProfile`` and their
		associated ``User``s.

		Accounts to be deleted are identified by searching for
		instances of ``RegistrationProfile`` with expired activation
		keys, and then checking to see if their associated ``User``
		instances have the field ``is_active`` set to ``False``; any
		``User`` who is both inactive and has an expired activation
		key will be deleted.

		It is recommended that this method be executed regularly as
		part of your routine site maintenance; the file
		``bin/delete_expired_users.py`` in this application provides a
		standalone script, suitable for use as a cron job, which will
		call this method.

		Regularly clearing out accounts which have never been
		activated serves two useful purposes:

		1. It alleviates the ocasional need to reset a
		   ``RegistrationProfile`` and/or re-send an activation email
		   when a user does not receive or does not act upon the
		   initial activation email; since the account will be
		   deleted, the user will be able to simply re-register and
		   receive a new activation key.

		2. It prevents the possibility of a malicious user registering
		   one or more accounts and never activating them (thus
		   denying the use of those usernames to anyone else); since
		   those accounts will be deleted, the usernames will become
		   available for use again.

		If you have a troublesome ``User`` and wish to disable their
		account while keeping it in the database, simply delete the
		associated ``RegistrationProfile``; an inactive ``User`` which
		does not have an associated ``RegistrationProfile`` will not
		be deleted.

		"""
		for profile in self.all():
			if profile.activation_key_expired():
				user = profile.user
				if not user.is_active:
					# Removing the ``User`` will remove the ``RegistrationProfile``, too.
					user.delete()

class RegistrationProfile(models.Model):
	"""
	A simple profile which stores an activation key for use during
	user account registration.

	Generally, you will not want to interact directly with instances
	of this model; the provided manager includes methods
	for creating and activating new accounts, as well as for cleaning
	out accounts which have never been activated.

	While it is possible to use this model as the value of the
	``AUTH_PROFILE_MODULE`` setting, it's not recommended that you do
	so. This model is intended solely to store some data needed for
	user registration, and can do that regardless of what you set in
	``AUTH_PROFILE_MODULE``, so if you want to use user profiles in a
	project, it's far better to develop a customized model for that
	purpose and just let this one handle registration.

	"""
	user = models.ForeignKey(User, unique=True, verbose_name=_('user'))
	activation_key = models.CharField(_('activation key'), max_length=40)

	objects = RegistrationManager()

	class Meta:
		verbose_name = _('registration profile')
		verbose_name_plural = _('registration profiles')

	#class Admin(admin.ModelAdmin):
	#	list_display = ('__unicode__', 'activation_key_expired')
	#	search_fields = ('user__username', 'user__first_name')

	def __unicode__(self):
		return _('Registration information for %(username)s') % {'username' : self.user.username}

	def activation_key_expired(self):
		"""
		Determines whether this ``RegistrationProfile``'s activation
		key has expired.

		Returns ``True`` if the key has expired, ``False`` otherwise.

		Key expiration is determined by the setting
		``ACCOUNT_ACTIVATION_DAYS``, which should be the number of
		days a key should remain valid after an account is registered.

		"""
		expiration_date = datetime.timedelta(days=getattr(settings, 'ACCOUNT_ACTIVATION_DAYS', 5))
		return self.user.date_joined + expiration_date <= datetime.datetime.now()
	activation_key_expired.boolean = True

#admin.site.register(RegistrationProfile, RegistrationProfile.Admin)
