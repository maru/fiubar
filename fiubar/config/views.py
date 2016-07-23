# -*- coding: utf-8 -*-
from django.shortcuts import render

def home(request):
	"""
	Home page: choose template based on logged-in user / new user.
	"""
	if request.user.is_authenticated():
		template_file = 'pages/home.html'	
	else:
		template_file = 'pages/index.html'

	context = { 'slug' : 'home' }
	return render(request, template_file, context)
