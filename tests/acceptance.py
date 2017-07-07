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

from arcadiamock import __VERSION__
from arcadiamock.utils import execute
from arcadiamock.client import Client
from arcadiamock.servicegraphs import ServiceGraph, Node, Component


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
        about = self.client.about()
        self.assertEqual(__VERSION__, about.version)

    def test_fetch_and_then_retrieve_service_graphs(self):
        self._ensure_server_is_alive()

        # Retrieve the list of service graphs
        service_graphs = self.client.service_graphs()

        # Register a new service graph
        service_graph = ServiceGraph(
            nodes=[Node(50, "foooooo!")],
            policy=[])
        self.client.register_service_graph(service_graph)

        # Register the list of service graphs
        new_service_graphs = self.client.service_graphs()

        self.assertEqual(len(new_service_graphs), len(service_graphs) + 1)

    def test_register_and_fetch_component(self):
        self._ensure_server_is_alive()

        # Fetch the number of registered components
        old_component_count = self.client.components().count

        # Create and push a new component named foo
        cnid = "foo"
        local_component = Component(cnid=cnid)
        self.client.register_component(local_component)

        # Check the number of components has been incremented
        self.assertEqual(old_component_count + 1,
                         self.client.components().count)

        # Check that the new component is accessible
        remote_component = self.client.component_with_CNID(cnid)
        self.assertEqual(local_component.cnid, remote_component.cnid)

    def _ensure_server_is_alive(self):
        if self.server.poll() is not None:
            message = self.ERROR_SERVER_IS_DOWN.format(log=self.LOG_FILE)
            self.fail(message)

