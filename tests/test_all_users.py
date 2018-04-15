# -*- coding: utf-8 -*-
from common import FiubarTest

class NewVisitorTest(FiubarTest):

    def test_it_worked(self):
        self.browser.get(self.server_name)
        self.assertIn('Fiubar', self.browser.title)
