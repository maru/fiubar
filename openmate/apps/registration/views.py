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
from registration.forms import RegistrationFormUniqueEmail, PasswordResetForm, PasswordChangeForm
from registration.models import RegistrationProfile
from django.contrib.auth.models import User

def activate(request, activation_key, template_name='registration/activate.html'):
	"""
	Activates a ``User``'s account, if their key is valid and hasn't
	expired.

	By default, uses the template ``registration/activate.html``; to
	change this, pass the name of a template as the keyword argument
	``template_name``.

	**Context:**

	account
		The ``User`` object corresponding to the account, if the
		activation was successful. ``False`` if the activation was not
		successful.

	expiration_days
		The number of days for which activation keys stay valid after
		registration.

	**Template:**

	registration/activate.html or ``template_name`` keyword argument.

	"""
	activation_key = activation_key.lower() # Normalize before trying anything with it.
	account = RegistrationProfile.objects.activate_user(activation_key)

	if (account):
		logger.info("%s - account-activate: user %s" %(request.META.get('REMOTE_ADDR'), account))
	else:
		logger.error("%s - account-activate: activation_key %s" %(request.META.get('REMOTE_ADDR'), activation_key))
	return render_to_response(template_name,
							  { 'account': account,
								'expiration_days': getattr(settings, 'ACCOUNT_ACTIVATION_DAYS', 5) },
							  context_instance=RequestContext(request))


def register(request, success_url='/account/register/complete/',
			 form_class=RegistrationFormUniqueEmail, profile_callback=None,
			 template_name='registration/registration_form.html'):
	"""
	Allows a new user to register an account.

	Following successful registration, redirects to either
	``/accounts/register/complete/`` or, if supplied, the URL
	specified in the keyword argument ``success_url``.

	By default, ``registration.forms.RegistrationForm`` will be used
	as the registration form; to change this, pass a different form
	class as the ``form_class`` keyword argument. The form class you
	specify must have a method ``save`` which will create and return
	the new ``User``, and that method must accept the keyword argument
	``profile_callback`` (see below).

	To enable creation of a site-specific user profile object for the
	new user, pass a function which will create the profile object as
	the keyword argument ``profile_callback``. See
	``RegistrationManager.create_inactive_user`` in the file
	``models.py`` for details on how to write this function.

	By default, uses the template
	``registration/registration_form.html``; to change this, pass the
	name of a template as the keyword argument ``template_name``.

	**Context:**

	form
		The registration form.

	**Template:**

	registration/registration_form.html or ``template_name`` keyword
	argument.

	"""
	if request.method == 'POST':
		form = form_class(request.POST)
		logger.debug("%s - account-register: username: '%s', first_name: '%s', last_name: '%s', email: '%s', tipo_verificacion: '%s', verificacion: '%s',  tipo_request_auth: '%s', request_auth: '%s'" % (request.META.get('REMOTE_ADDR'), form.data['username'], form.data['first_name'], form.data['last_name'], form.data['email'], form.data['tipo_verificacion'], form.data['verificacion'], form.data['tipo_request_auth'], form.data['request_auth']))
		if form.is_valid():
			# new_user = form.save(profile_callback=profile_callback)
			# return HttpResponseRedirect(success_url)
			if form.is_request_auth():
				# User is not alumno.
				send_email = False
				activation_email = form.cleaned_data['email']
			else:
				# User is alumno or has an email account.
				if form.is_account():
					# User has an email account.
					if settings.CHECK_PADRON.is_registered(form.cleaned_data['verificacion']):
						form.errors['verificacion'] = [_(u'Cuenta ya utilizada. Por favor contactate con nosotros \
								si creés que alguien utilizó tu cuenta.')]
						#logger.error("%s - check_padron %s ('%s', '%s', '%s')" % (request.META.get('REMOTE_ADDR'), 'ALREADY USED', form.cleaned_data['verificacion'], form.data['first_name'], form.data['last_name']))
					else:
						activation_email = form.cleaned_data['verificacion'] + '@fi.uba.ar'

				# Check padron
				elif form.is_padron():
					# Check verificacion repetido
					verificacion_error, log_message = settings.CHECK_PADRON.check_padron(form.cleaned_data['verificacion'], form.data['first_name'], form.data['last_name'])
					if verificacion_error:
						logger.error("%s - check_padron %s ('%s', '%s', '%s')" % (request.META.get('REMOTE_ADDR'), log_message, form.cleaned_data['verificacion'], form.data['first_name'], form.data['last_name']))
						form.errors['verificacion'] = [verificacion_error]
					else:
					    logger.info("%s - check_padron %s ('%s', '%s', '%s')" % (request.META.get('REMOTE_ADDR'), log_message, form.cleaned_data['verificacion'], form.data['first_name'], form.data['last_name']))
					activation_email = form.cleaned_data['email']
				send_email = True

			if len(form.errors) == 0:
				# Register new user
				new_user = RegistrationProfile.objects.create_inactive_user(username=form.cleaned_data['username'],
							  password=form.cleaned_data['password'], first_name=form.cleaned_data['first_name'],
							  last_name=form.cleaned_data['last_name'], email=activation_email, send_email=send_email)
				logger.info("%s - new_user ('%s', '%s')" % (request.META.get('REMOTE_ADDR'), new_user.username, new_user.email))
				if form.is_account():
					# Save user's email.
					new_user.email = form.cleaned_data['email']
					new_user.save()

				from django.core.mail import send_mail
				current_site = Site.objects.get_current()

				subject = _(u'[%s] New user' % current_site.name)
				message = render_to_string('registration/new_user_email.html',
										   { 'new_user': form.cleaned_data,
											 'site_url': 'http://%s/' % current_site.domain,
											 'site_name': current_site.name, })
				send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [a[1] for a in settings.MANAGERS])

				if send_email:
					settings.CHECK_PADRON.save_user(form.cleaned_data['verificacion'], form.data['first_name'], form.data['last_name'])
				return render_to_response('registration/registration_complete.html',
										  { 'send_email': send_email,
											'activation_email' : activation_email, },
										  context_instance=RequestContext(request))

			"""
			request_auth = form.cleaned_data['request_auth']

			return render_to_response('registration_complete.html',
									  { 'send_email': send_email },
									  context_instance=RequestContext(request))
			return HttpResponseRedirect(success_url)
			"""
	else:
		form = form_class()
	return render_to_response(template_name, { 'form': form },
							  context_instance=RequestContext(request))



