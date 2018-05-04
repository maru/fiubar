# -*- coding: utf-8 -*-
from common import FiubarTest


class NewUserTest(FiubarTest):

    def test_it_worked(self):
        self.browser.get(self.server_name)

        assert 'Fiubar' in browser.title
        self.assertIn('Fiubar', self.browser.title)

    def test_new_user(self):
        self.browser.get(self.server_name)

        # Selecciona carrera
        # Selecciona plancarrera
        # Selecciona orientacion
        # Selecciona materias aprobadas
        # Ingresa fecha de cursada
        # Ingresa fecha de aprobada
        # Selecciona materias a final
        # Selecciona materias cursando
        # Crea un usuario
