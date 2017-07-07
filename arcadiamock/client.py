#
# ARCADIA Mocks
#
# Copyright (C) 2017 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#


from requests import Request, Session
from requests.exceptions import ConnectionError
from time import sleep

from arcadiamock.adapters import XMLParser, XMLPrinter


class Client(object):

    DEFAULT_HOST_NAME = "localhost"
    DEFAULT_PORT = 5000

    def __init__(self, hostname=None, port=None):
        self._hostname = hostname or self.DEFAULT_HOST_NAME
        self._port = port or self.DEFAULT_PORT
        self._headers = {
            "accept": "application/xml"
        }
        self._parse = XMLParser()
        self._formatter = XMLPrinter()

    def register_service_graph(self, service_graph):
        xml = service_graph.accept(self._formatter)
        response = self._fetch(resource=self._url_of("/register"),
                               method="POST",
                               payload=xml.as_text())
        response.raise_for_status()

    def component_with_CNID(self, cnid):
        resource = "/components/{0}".format(cnid)
        url = self._url_of(resource)
        response = self._fetch(url)
        return self._parse.graph_node_from(response.text)

    def service_graphs(self):
        response = self._fetch(self._url_of("/service_graphs"))
        return self._parse.service_graphs_from(response.text)

    def about(self):
        response = self._fetch(self._url_of("/about"))
        return self._parse.about_from(response.text)

    def _url_of(self, page):
        return self._base_url + page

    @property
    def _base_url(self):
        URL = "http://{hostname}:{port}"
        return URL.format(
            hostname=self._hostname,
            port=self._port)

    def _fetch(self, resource, method="GET", payload=None):
        attempt = self.MAX_ATTEMPTS
        while attempt >= 0:
            try:
                attempt -= 1
                request = Request(method, resource, headers=self._headers, data=payload)
                return Session().send(request.prepare())
            except ConnectionError:
                sleep(self.DELAY)

        message = self.ERROR_CANNOT_GET_PAGE.format(page=page,
                                                    attempts=self.MAX_ATTEMPTS)
        raise RuntimeError(message)

    MAX_ATTEMPTS = 3
    DELAY = 5
    ERROR_CANNOT_GET_PAGE = "Cannot access '{page}' ({attempts} attempts)."
