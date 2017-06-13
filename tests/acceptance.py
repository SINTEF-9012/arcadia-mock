#
# ARCADIA Mocks
#
# Copyright (C) 2017 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#


from unittest import TestCase
from requests import get
from subprocess import Popen
from time import sleep


class Pages:
    BASE = "http://localhost:5000"
    ABOUT = BASE + "/about"


class AcceptanceTests(TestCase):
    """
    Start the server, listening on localhost, and send HTTP requests
    and check responses.
    """
    
    MAX_ATTEMPTS = 3
    DELAY = 5

    def setUp(self):
        self.log_file = open("acceptance.log", "w")
        self.arcadia_mocks = Popen(["arcadiamock"], 
                                   stdout=self.log_file, 
                                   stderr=self.log_file)

    def tearDown(self):
        self.log_file.close()
        self.arcadia_mocks.kill()

    def test_about(self):
        response = self._fetch(Pages.ABOUT)
        self.assertEqual(200, response.status_code)

    def _fetch(self, page):
        attempt = self.MAX_ATTEMPTS
        while attempt >= 0:
            try:
                response = get(page)
                return response
            except:
                sleep(self.DELAY)
                attempt -= 1
        message = "Cannot access '{page}' after {attempts} attempts.".format(
            page=page,
            attempts=self.MAX_ATTEMPTS)
        raise RuntimeError(message)
                



        
