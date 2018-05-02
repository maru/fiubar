import os
import tempfile

from django.test import TestCase

from . import common


class SettingsTestCase(TestCase):
    secret_file = None

    def setUp(self):
        if os.getenv("FIUBAR_SECRET_FILE"):
            self.secret_file = os.getenv("FIUBAR_SECRET_FILE")
            del os.environ["FIUBAR_SECRET_FILE"]

    def tearDown(self):
        if self.secret_file:
            os.environ["FIUBAR_SECRET_FILE"] = self.secret_file

    def test_secret_file_is_none(self):
        """ No secret file """
        common.secrets = common.read_secret_file()
        self.assertEqual(common.secrets, {})

    def test_secret_file(self):
        """ Use a secret file, correct JSON format """
        fp = tempfile.NamedTemporaryFile(mode='w')
        fp.write('{ "DJANGO_SECRET_KEY": "my_django_key" }')
        fp.seek(0)

        os.environ["FIUBAR_SECRET_FILE"] = fp.name

        common.secrets = common.read_secret_file()
        self.assertEqual(common.get_secret('DJANGO_SECRET_KEY'),
                         'my_django_key')
        fp.close()

    def test_secret_file_bad_json(self):
        """ Use a secret file, bad JSON format """
        fp = tempfile.NamedTemporaryFile(mode='w')
        fp.write('DJANGO_SECRET_KEY=my_django_key')
        fp.seek(0)

        os.environ["FIUBAR_SECRET_FILE"] = fp.name

        bad_json = False
        common.secrets = {}
        try:
            common.secrets = common.read_secret_file()
        except ValueError:
            bad_json = True
        self.assertEqual(bad_json, True)
        self.assertEqual(common.secrets, {})
        fp.close()

    def test_secret_setting_true_false(self):
        """ Convert setting value from string "True" and "False" to boolean """
        fp = tempfile.NamedTemporaryFile(mode='w')
        fp.write('{ "DEBUG_TRUE": "True", "DEBUG_FALSE": "False" }')
        fp.seek(0)

        os.environ["FIUBAR_SECRET_FILE"] = fp.name

        common.secrets = common.read_secret_file()
        self.assertTrue(common.get_secret('DEBUG_TRUE'))
        self.assertFalse(common.get_secret('DEBUG_FALSE'))
        fp.close()
