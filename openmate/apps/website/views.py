# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponseServerError
from django.template import RequestContext
from django.core.urlresolvers import reverse

dict_data = {}

def index(request):
	"""Home page."""
	if request.user.is_authenticated():
		if request.path == '/':
			return HttpResponseRedirect(reverse('website-home'))
		template_file = 'website/home.html'
	else:
		# Create cookie session
		request.session.set_test_cookie()
		template_file = 'website/index.html'
	return render_to_response(template_file,
							  context_instance=RequestContext(request))

# Custom 404 and 500 views
from django.views import defaults
from django.template import loader, TemplateDoesNotExist

def page_not_found(request):
	template_name = '404.html'
	module = request.path.split('/')[1]
	try:
		template_name = module + '/404.html'
		t = loader.get_template(template_name)
	except TemplateDoesNotExist:
		template_name = '404.html'
	return defaults.page_not_found(request, template_name)

def server_error(request, template_name = 'website/500.html'):
	t = loader.get_template(template_name)
	return HttpResponseServerError(t.render(RequestContext(request)))
