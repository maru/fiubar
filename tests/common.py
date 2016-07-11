# -*- coding: utf-8 -*-

import os
import unittest
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

FIREFOX_PATH = os.getenv('TEST_FIREFOX_PATH', '/usr/local/bin/firefox-44.0/firefox')
SERVER_NAME = os.getenv('TEST_SERVER_NAME', 'http://localhost:8000/')

class FiubarTest(unittest.TestCase):
    firefox_path = FIREFOX_PATH
    server_name = SERVER_NAME

    def __init__(self, methodName='runTest'):
        super(FiubarTest, self).__init__(methodName)
        self.browser = None

    def setUp(self):
        self.browser = webdriver.Firefox(firefox_binary=FirefoxBinary(self.firefox_path))
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()
