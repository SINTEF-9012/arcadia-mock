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
from requests.exceptions import ConnectionError
from subprocess import Popen
from time import sleep
from signal import SIGTERM
from sys import platform
from os import kill

from arcadiamock.utils import spawn

class Pages:
    BASE = "http://localhost:5000"
    ABOUT = BASE + "/about"
    

class AcceptanceTests(TestCase):
    """
    Start the server, listening on localhost, and send HTTP requests
    and check responses.
    """
    
    SERVER_START_COMMAND = ["arcadiamock"]
    LOG_FILE = "acceptance.log"
    ERROR_SERVER_IS_DOWN = "The arcadia-mock server has stopped. Check '{log}'"
    ERROR_CANNOT_GET_PAGE = "Cannot access '{page}' after {attempts} attempts."

    MAX_ATTEMPTS = 3
    DELAY = 5

    def setUp(self):
        self.log_file = open(self.LOG_FILE, "w")
        self.server = spawn(self.SERVER_START_COMMAND, self.log_file)

    def tearDown(self): 
        self.log_file.close()
        self.server.terminate()

    def test_about(self):
        response = self._fetch(Pages.ABOUT)
        self.assertEqual(200, response.status_code)

    def _fetch(self, page):
        attempt = self.MAX_ATTEMPTS
        while attempt >= 0:
            try:
                attempt -= 1
                self._ensure_server_is_alive()
                return get(page)
            except ConnectionError:
                sleep(self.DELAY)
        message = self.ERROR_CANNOT_GET_PAGE.format(page=page, attempts=self.MAX_ATTEMPTS)
        self.fail(message)
                
    def _ensure_server_is_alive(self):
        if self.server.poll() is not None:
            message = self.ERROR_SERVER_IS_DOWN.format(log=self.LOG_FILE)
            self.fail(message)



        
