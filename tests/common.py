import os
import unittest

from selenium import webdriver
from selenium.webdriver.firefox import firefox_binary


FIREFOX_PATH = os.getenv('TEST_FIREFOX_PATH', '/usr/bin/firefox')
SERVER_NAME = os.getenv('TEST_SERVER_NAME', 'http://localhost:8000/')

class FiubarTest(unittest.TestCase):
    """
    Base class for tests using selenium.
    """
    def __init__(self, methodName='runTest'):
        super(FiubarTest, self).__init__(methodName)
        self.browser = None
        self.server_name = SERVER_NAME

    def setUp(self):
        binary = firefox_binary.FirefoxBinary(FIREFOX_PATH)
        self.browser = webdriver.Firefox(firefox_binary=binary)
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()
