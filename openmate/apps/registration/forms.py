# -*- coding: utf-8 -*-
"""
Copyright (c) 2007, James Bennett
Copyright (c) 2008, OpenMate - Some changes introduced

Form and validation code for user registration.

"""


import re

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

# I put this on all required fields, because it's easier to pick up
# on them with CSS or JavaScript if they have a class of "required"
# in the HTML. Your mileage may vary.
attrs_dict = { 'class': 'required' }


username_re = re.compile(r'^\w{2,30}$')
# password_re = re.compile(r'^.*(?=.{6,})(?=.*\d)(?=.*[a-z]).*$')
password_re = re.compile(r'^.{6,}.*$')
padron_re = re.compile(r'^([Bb][0-9]{4}|[0-9]{5})$')
account_re = re.compile(r'^[a-z]{2,30}$')
name_re = re.compile(u"^[\wñÑçÇ' -]{2,}$")

class RegistrationForm(forms.Form):
	"""
	Form for registering a new user account.

	Validates that the password is entered twice and matches,
	and that the username is not already taken.

	@OpenMate
	22-10-2007	Form changed, commented tos

	"""
	TIPO_VERIFICACION = (
		( 'p', u'Padrón'),
		( 'u', u'Usuario @fi.uba.ar'),
	)
	TIPO_REQUEST_AUTH = (
		( '',  u'--------------'),
		( 'g', u'Soy graduado/a'),
		( 'd', u'Soy docente'),
		( 't', u'Soy no docente'),
		( 'c', u'Curso el CBC'),
		( 'e', u'No reconoció mi padrón'),
		( 'o', u'Otro'),
	)
	username = forms.CharField( max_length=30,
								widget=forms.TextInput(attrs=attrs_dict),
								label=_('Username'),
				   help_text=_(u'¡El que a vos te guste! Números, letras y guión bajo solamente. \
				   Entre 2 y 30 caracteres.'))
	tipo_verificacion = forms.ChoiceField(choices=TIPO_VERIFICACION, initial='p')
	verificacion = forms.CharField( #max_length=10,
								widget=forms.TextInput(attrs=attrs_dict),
								label=_(u'Padrón'), required=False,
				   help_text=_(u'Ingresá tu padrón o usuario de mail @fi.uba.ar.'))
	tipo_request_auth = forms.ChoiceField(choices=TIPO_REQUEST_AUTH, initial='', required=False)
	request_auth = forms.CharField(widget=forms.Textarea(attrs={'class':'request-auth', 'rows':'2', 'cols':'5'}),
								   required=False)
	first_name = forms.CharField(max_length=30,
								widget=forms.TextInput(attrs=attrs_dict),
								label=_('Nombre'),
				   help_text=_(u'Tu nombre completo, es importante para validar junto a tu padrón.'))
	last_name = forms.CharField(max_length=30,
								widget=forms.TextInput(attrs=attrs_dict),
								label=_('Apellido'),
				   help_text=_(u'Tu apellido, sin acentos, es importante para validar junto a tu padrón.'))
	email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=200)),
								label=_('Email address'),
				   help_text=_(u'Ingresá tu email, imprescindible para resetear tu contraseña y para los grupos.'))
	password = forms.CharField( widget=forms.PasswordInput(attrs=attrs_dict),
								label=_(u'Contraseña'),
				   help_text=_(u'Tu contraseña debe tener por lo menos 6 caracteres.')) #, al menos una letra Y un número.'))
	password_verify = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict),
								label=_(u'Confirmar contraseña'),
				   help_text=_(u'Reingresá tu contraseña, para verificar.'))
	#tos = forms.BooleanField(widget=forms.CheckboxInput(attrs=attrs_dict), required=False,
	#						 label=u'I have read and agree to the Terms of Service')

	def clean_username(self):
		"""
		Validates that the username is alphanumeric and is not already
		in use.

		"""
		if 'username' in self.cleaned_data:
			if not username_re.search(self.cleaned_data['username']):
				# raise forms.ValidationError(_('Usernames can only contain letters, numbers and underscores'))
				raise forms.ValidationError(_(u'El nombre de usuario solo puede contener letras, números y guiones bajos'))
			try:
				user = User.objects.get(username__iexact=self.cleaned_data['username'])
			except User.DoesNotExist:
				return self.cleaned_data['username']
			# raise forms.ValidationError(_('This username is already taken. Please choose another.'))
			raise forms.ValidationError(_(u'Ese nombre de usuario ya está asignado. Por favor eligí otro.'))

	def clean_first_name(self):
		"""
		Validates that the first_name matches the required characters and
		length.

		"""
		if not name_re.search(self.cleaned_data['first_name']):
			raise forms.ValidationError(_(u'Ingresá tu nombre sin acentos.'))
		return self.cleaned_data['first_name']

	def clean_last_name(self):
		"""
		Validates that the last_name matches the required characters and
		length.

		"""
		if not name_re.search(self.cleaned_data['last_name']):
			raise forms.ValidationError(_(u'Ingresá tu apellido sin acentos.'))
		return self.cleaned_data['last_name']

	def clean_password(self):
		"""
		Validates that the password matches the required characters and
		length.

		"""
		if not password_re.search(self.cleaned_data['password']):
			raise forms.ValidationError(_(u'Contraseña no válida. Tu contraseña debe tener por lo menos 6 caracteres.'))
			#					 sin espacios. Debe contener al menos una letra Y un número.'))
		return self.cleaned_data['password']

	def clean_password_verify(self):
		"""
		Validates that the two password inputs match.

		"""
		if 'password' in self.cleaned_data and 'password_verify' in self.cleaned_data and \
		   self.cleaned_data['password'] == self.cleaned_data['password_verify']:
			return self.cleaned_data['password_verify']
		# raise forms.ValidationError(_('You must type the same password each time'))
		raise forms.ValidationError(_(u'Debés tipear la misma contraseña cada vez'))


	def clean_verificacion(self):
		"""
		Validates

		"""
		verification_data = self.cleaned_data['verificacion']
		# User requests authorization
		if self.is_request_auth():
			return verification_data
		# Field empty.
		if len(verification_data) == 0:
			raise forms.ValidationError(_(u'Este campo es obligatorio.'))

		# Check padrón
		if self.is_padron():
			if padron_re.search(verification_data):
				return verification_data
		# Check account
		elif self.is_account():
			if account_re.search(verification_data):
				return verification_data
		# Data is not valid
		raise forms.ValidationError(_(u'Ingresar un valor válido. '))

	def clean_request_auth(self):
		"""
		request_auth is required only if tipo_request_auth is 'Otro'.

		"""
		if (self.data['tipo_request_auth'] == 'o'):
			if len(self.cleaned_data['request_auth']) == 0:
				raise forms.ValidationError(_(u'Por favor, escriba la razón de su registración.'))
		# Make 72 chars lines
		return self.cleaned_data['request_auth']

	def is_padron(self):
		return (self.cleaned_data['tipo_verificacion'] == 'p')

	def is_account(self):
		return (self.cleaned_data['tipo_verificacion'] == 'u')

	def is_request_auth(self):
		return (self.data['tipo_request_auth'] != '')

class RegistrationFormTermsOfService(RegistrationForm):
	"""
	Subclass of ``RegistrationForm`` which adds a required checkbox
	for agreeing to a site's Terms of Service.

	"""
	tos = forms.BooleanField(widget=forms.CheckboxInput(attrs=attrs_dict),
							 label=_(u'I have read and agree to the Terms of Service'))

	def clean_tos(self):
		"""
		Validates that the user accepted the Terms of Service.

		"""
		if self.cleaned_data.get('tos', False):
			return self.cleaned_data['tos']
		raise forms.ValidationError(_(u'You must agree to the terms to register'))


class RegistrationFormUniqueEmail(RegistrationForm):
	"""
	Subclass of ``RegistrationForm`` which enforces uniqueness of
	email addresses.

	"""
	def clean_email(self):
		"""
		Validates that the supplied email address is unique for the
		site.

		"""
		try:
			user = User.objects.get(email__exact=self.cleaned_data['email'])
		except User.DoesNotExist:
			return self.cleaned_data['email']
		# raise forms.ValidationError(_(u'This email address is already in use. Please supply a different email address.'))
		raise forms.ValidationError(_(u'Esa dirección de e-mail ya está en uso. Por favor proveé otra dirección.'))

class RegistrationFormNoFreeEmail(RegistrationForm):
	"""
	Subclass of ``RegistrationForm`` which disallows registration with
	email addresses from popular free webmail services; moderately
	useful for preventing automated spam registrations.

	To change the list of banned domains, subclass this form and
	override the attribute ``bad_domains``.

	"""
	bad_domains = ['aim.com', 'aol.com', 'email.com', 'gmail.com',
				   'googlemail.com', 'hotmail.com', 'hushmail.com',
				   'msn.com', 'mail.ru', 'mailinator.com', 'live.com']

	def clean_email(self):
		"""
		Checks the supplied email address against a list of known free
		webmail domains.

		"""
		email_domain = self.cleaned_data['email'].split('@')[1]
		if email_domain in self.bad_domains:
			raise forms.ValidationError(_(u'Registration using free email addresses is prohibited. Please supply a different email address.'))
		return self.cleaned_data['email']

class PasswordResetForm(forms.Form):
	email = forms.EmailField(max_length=200)

	def clean_email(self):
		email = self.cleaned_data.get('email', '')
		try:
			self.user = User.objects.get(email__iexact=email)
		except:
			raise forms.ValidationError(_("That e-mail address doesn't have an associated user account. Are you sure you've registered?"))
		return email

class PasswordChangeForm(forms.Form):
	password = forms.CharField(widget=forms.PasswordInput(), label=_('Password'),
		help_text=_(u'Tu contraseña debe tener por lo menos 6 caracteres, al menos una letra Y un número.'))
	password_verify = forms.CharField(widget=forms.PasswordInput(), label=_('Password (again, to catch typos)'),
				   help_text=_(u'Reingresá tu contraseña, para verificar.'))

	def clean_password(self):
		"""
		Validates that the password matches the required characters and
		length.

		"""
		if not password_re.search(self.cleaned_data['password']):
			raise forms.ValidationError(_(u'Contraseña no válida. Tu contraseña debe tener por lo menos 6 caracteres, \
								 sin espacios. Debe contener al menos una letra Y un número.'))
		return self.cleaned_data['password']

	def clean_password_verify(self):
		"""
		Validates that the two password inputs match.

		"""
		if 'password' in self.cleaned_data and 'password_verify' in self.cleaned_data and \
		   self.cleaned_data['password'] == self.cleaned_data['password_verify']:
			return self.cleaned_data['password_verify']
		# raise forms.ValidationError(_('You must type the same password each time'))
		raise forms.ValidationError(_(u'Debés tipear la misma contraseña cada vez'))
