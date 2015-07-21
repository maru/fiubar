# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template, redirect_to
from contact_form.views import contact_form

urlpatterns = patterns('',

	url(r'^fiubar/$', direct_to_template,
		{'template' : 'about/fiubar.html'},
		name='about-fiubar'),

	url(r'^faq/$', direct_to_template,
		{'template' : 'about/faq.html'},
		name='about-faq'),

	url(r'^bugs/$', contact_form,
		{ 'template_name': 'about/bugs_form.html',
		  'success_url' : '/about/bugs/sent/' },
		name='about-bugs'),

	url(r'^bugs/sent/$', direct_to_template,
		{ 'template': 'about/bugs_form_sent.html' },
		name='about-bugs_sent'),

	url(r'^$', redirect_to,
		{'url' : '/about/fiubar/'}),

	url(r'^contact/$', contact_form,
		{ 'template_name': 'about/contact_form.html',
		  'success_url' : '/about/contact/sent/' },
		name='about-contact'),

	url(r'^contact/sent/$', direct_to_template,
		{ 'template': 'about/contact_form_sent.html' },
		name='about-contact_sent'),

	#url(r'^ideas/$', 'ideas',
	#	name='about-ideas'),

	#url(r'^brainstorm/$', direct_to_template,
	#	{'template' : 'about/brainstorm.html'},
	#	name='about-brainstorm'),

	#url(r'^participate/$', 'participate_form',
	#	name='about-participate'),

)
