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
from requests import get, head
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


    def setUp(self):
        self.log_file = open("acceptance.log", "w")
        self.arcadia_mocks = Popen(["arcadiamock"], 
                                   stdout=self.log_file, 
                                   stderr=self.log_file)
        self._wait_for_arcadia_mocks()
        
    def _wait_for_arcadia_mocks(self):
        attempts = 3
        while attempts > 0:
            if head(Pages.ABOUT).status_code == 200: return
            attempts -= 1
            sleep(1)
        message = "Cannot start arcadiamock! Can't access '{page}'!".format(page=Pages.ABOUT)
        raise ValueError(message)

    def tearDown(self):
        self.log_file.close()
        self.arcadia_mocks.kill()

    def test_about(self):
        response = get(Pages.ABOUT)
        self.assertEqual(200, response.status_code)
        
