#
# ARCADIA Mocks
#
# Copyright (C) 2017 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#


from requests import get, Request, Session
from requests.exceptions import ConnectionError
from time import sleep


class Client(object):


    DEFAULT_HOST_NAME = "localhost"
    DEFAULT_PORT = 5000

    def __init__(self, hostname=None, port=None):
        self._hostname = hostname or self.DEFAULT_HOST_NAME
        self._port = port or self.DEFAULT_PORT
        self._headers = {
            "accept": "application/xml"
        }

    def service_graphs(self):
        response = self._fetch(self._url_of("/service_graphs"))
        return response

    def about(self):
        response = self._fetch(self._url_of("/about"))
        return response

    def _url_of(self, page):
        return self._base_url + page

    @property
    def _base_url(self):
        URL = "http://{hostname}:{port}"
        return URL.format(
            hostname=self._hostname,
            port=self._port)

    def _fetch(self, page, method="GET"):
        attempt = self.MAX_ATTEMPTS
        while attempt >= 0:
            try:
                attempt -= 1
                request = Request(method, page, headers=self._headers)
                return Session().send(request.prepare())
            except ConnectionError:
                sleep(self.DELAY)

        message = self.ERROR_CANNOT_GET_PAGE.format(page=page,
                                                    attempts=self.MAX_ATTEMPTS)
        raise RuntimeError(message)

    MAX_ATTEMPTS = 3
    DELAY = 5
    ERROR_CANNOT_GET_PAGE = "Cannot access '{page}' ({attempts} attempts)."
