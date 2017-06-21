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
from requests import get, Request, Session
from requests.exceptions import ConnectionError
from time import sleep

from arcadiamock.utils import execute


class Pages(object):

    URL = "http://{hostname}:{port}"
    DEFAULT_HOST_NAME = "localhost"
    DEFAULT_PORT = 5000

    def __init__(self, hostname=None, port=None):
        self._hostname = hostname or self.DEFAULT_HOST_NAME
        self._port = port or self.DEFAULT_PORT

    @property
    def service_graphs(self):
        return self._url_of("/service_graphs")

    @property
    def about(self):
        return self._url_of("/about")

    def _url_of(self, page):
        return self._base_url + page

    @property
    def _base_url(self):
        return self.URL.format(
            hostname=self._hostname,
            port=self._port)


class AcceptanceTests(TestCase):
    """
    Start the server, listening on localhost, and send HTTP requests
    and check responses.
    """

    PORT = 5000

    LOG_FILE = "acceptance.log"
    ERROR_SERVER_IS_DOWN = "The arcadia-mock server has stopped. Check '{log}'"
    ERROR_CANNOT_GET_PAGE = "Cannot access '{page}' ({attempts} attempts)."

    MAX_ATTEMPTS = 3
    DELAY = 5

    def setUp(self):
        self.pages = Pages(port=self.PORT)
        self.log_file = open(self.LOG_FILE, "w")
        self.server = execute(
            ["arcadiamock", "--name", "127.0.0.1", "--port", str(self.PORT)],
            self.log_file)

    def tearDown(self):
        self.log_file.close()
        self.server.terminate()

    def test_about(self):
        response = self._fetch(self.pages.about)
        self.assertEqual(200, response.status_code)

    def test_fetch_service_graphs_as_xml(self):
        headers = { "accept": "application/xml" }
        response = self._fetch(self.pages.service_graphs, headers=headers)
        self.assertEqual(200, response.status_code)
        self.assertEqual("<ServiceGraph><GraphNodeDescriptor><GraphNode><NID>12</NID><CNID>foo</CNID></GraphNode></GraphNodeDescriptor></ServiceGraph>", response.text)

    def _fetch(self, page, method="GET", headers=None):
        attempt = self.MAX_ATTEMPTS
        while attempt >= 0:
            try:
                attempt -= 1
                self._ensure_server_is_alive()
                request = Request(method, page, headers=headers)
                return Session().send(request.prepare())
            except ConnectionError:
                sleep(self.DELAY)

        message = self.ERROR_CANNOT_GET_PAGE.format(page=page,
                                                    attempts=self.MAX_ATTEMPTS)
        self.fail(message)

    def _ensure_server_is_alive(self):
        if self.server.poll() is not None:
            message = self.ERROR_SERVER_IS_DOWN.format(log=self.LOG_FILE)
            self.fail(message)

