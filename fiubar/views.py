# -*- coding: utf-8 -*-
from allauth.account.forms import LoginForm, SignupForm
from django.shortcuts import render


def home(request):
    """
    Home page: choose template based on logged-in user / new user.
    """
    context = {'slug': 'home'}
    if request.user.is_authenticated:
        template_file = 'pages/home.html'
    else:
        template_file = 'pages/index.html'
        forms = {'login': LoginForm,
                 'signup': SignupForm, }
        context.update({'forms': forms})

    return render(request, template_file, context)
