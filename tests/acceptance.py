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

    def tearDown(self):
        self.log_file.close()
        self.arcadia_mocks.kill()

    def test_about(self):
        about = "http://localhost:5000/about"
        response = get(about)
        self.assertEqual(200, response.status_code)
        
