# -*- coding: utf-8 -*-

from allauth.account.adapter import DefaultAccountAdapter


class SignupClosedAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return False
