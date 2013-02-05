# -*- coding: utf-8 -*-
import os
import sys
import unittest
import tempfile

from mega import Mega
from mega.exceptions import MegaIncorrectPasswordExcetion

class TestMega(unittest.TestCase):    
    def setUp(self):
        unittest.TestCase.setUp(self)
        email = os.environ.get('MEGAEMAIL') or sys.argv[0]
        password = os.environ.get('MEGAPASSWORD') or sys.argv[1]
        self.api_logged = Mega.from_credentials(email, password)
        self.api_ephemeral = Mega.from_ephemeral()

    def _check_file_exists(self, file_name, files):
        uploaded = False
        for f in files['f']:
            if isinstance(f['a'], dict):
                if f['a'].get('n') == file_name:
                    uploaded = True
        return uploaded

    def _test_upload_file(self, api):
        api.get_files()

        # Create temp file
        uFile, uFilePath = tempfile.mkstemp()
        os.write(uFile, "Does it work?")
        os.close(uFile)
        api.uploadfile(uFilePath)  # inception
        files = api.get_files()
        uploaded = self._check_file_exists('tests.py', files)
        self.assertEqual(MegaIncorrectPasswordExcetion, uploaded, True)
        
    def test_login_fail(self):
        with self.assertRaises(MegaIncorrectPasswordExcetion):
            Mega.from_credentials("valid@email.com", "test");
    
    def test_login_valid(self):
        Mega.from_credentials(self._email, self._password)
    
    def test_upload_file_logged(self):
        self._test_upload_file(self.api_logged)
    
    def test_upload_file_ephemeral(self):
        self._test_upload_file(self.api_ephemeral)

if __name__ == '__main__':
    unittest.main()
