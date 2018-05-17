# -*- coding: utf-8 -*-
from allauth.account.forms import LoginForm, SignupForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.base import TemplateView


class HomePageView(TemplateView):

    template_name = "pages/new.html"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            # self.template_name = 'pages/home.html'
            # Redireccionamos directo a la lista de materias
            return HttpResponseRedirect(reverse('facultad:home'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({'slug': 'home',
                        'forms': {'login': LoginForm,
                                  'signup': SignupForm}
                        })
        return context
