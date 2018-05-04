# -*- coding: utf-8 -*-
from common import FiubarTest


class SigninTest(FiubarTest):

    def test_signin(self):
        self.browser.get(self.server_name)

        # Selecciona carrera
        # Selecciona plancarrera
        # Selecciona orientacion
        # Selecciona materias aprobadas
        # Ingresa fecha de cursada
        # Ingresa fecha de aprobada
        # Selecciona materias a final
        # Selecciona materias cursando
        # Inicia sesión

    def test_signin_bad_password(self):
        self.browser.get(self.server_name)

        # Selecciona carrera
        # Selecciona plancarrera
        # Selecciona orientacion
        # Selecciona materias aprobadas
        # Ingresa fecha de cursada
        # Ingresa fecha de aprobada
        # Selecciona materias a final
        # Selecciona materias cursando
        # Inicia sesión, error en password
        # Inicia sesión, error en usuario
