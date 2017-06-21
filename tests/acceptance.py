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

from arcadiamock.utils import execute
from arcadiamock.client import Client



class AcceptanceTests(TestCase):
    """
    Start the server, listening on localhost, and send HTTP requests
    and check responses.
    """

    PORT = 5000

    LOG_FILE = "acceptance.log"
    ERROR_SERVER_IS_DOWN = "The arcadia-mock server has stopped. Check '{log}'"


    def setUp(self):
        self.log_file = open(self.LOG_FILE, "w")
        self.server = execute(
            ["arcadiamock", "--name", "127.0.0.1", "--port", str(self.PORT)],
            self.log_file)
        self.client = Client(hostname="127.0.0.1", port=self.PORT)

    def tearDown(self):
        self.log_file.close()
        self.server.terminate()

    def test_fetch_about_information(self):
        self._ensure_server_is_alive()
        response = self.client.about()
        self.assertEqual(200, response.status_code)

    def test_fetch_service_graphs_as_xml(self):
        self._ensure_server_is_alive()
        response = self.client.service_graphs()
        self.assertEqual(200, response.status_code)
        self.assertEqual("<ServiceGraph><GraphNodeDescriptor><GraphNode><NID>12</NID><CNID>foo</CNID></GraphNode></GraphNodeDescriptor></ServiceGraph>", response.text)

    def _ensure_server_is_alive(self):
        if self.server.poll() is not None:
            message = self.ERROR_SERVER_IS_DOWN.format(log=self.LOG_FILE)
            self.fail(message)

