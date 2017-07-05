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
from mock import MagicMock


from arcadiamock.servicegraphs import *


class ServiceGraphTests(TestCase):

    def setUp(self):
        self.graph = ServiceGraph()

    def test_nodes(self):
        self.assertEqual(0, len(self.graph.nodes))

    def test_add_one_node(self):
        new_node = Node()
        self.graph.add_node(new_node)
        self.assertEqual(1, len(self.graph.nodes))

    def test_add_runtime_policy(self):
        new_policy = Policy()
        self.graph.policy = new_policy
        self.assertIs(new_policy, self.graph.policy)

    def test_add_metadata(self):
        metadata = MetaData()
        self.graph.metadata = metadata
        self.assertIs(metadata, self.graph.metadata)

    def test_visitor(self):
        visitor = MagicMock(Visitor)
        self.graph.accept(visitor)
        visitor.visit_service_graph.called_once_with(self.graph.nodes, None, None)


class ArcadiaMockTests(TestCase):

    def setUp(self):
        self.store = Store()

    def test_add_service_graphs(self):
        self.assertEqual(0, self.store.all_service_graphs().count)

        service_graph = ServiceGraph()
        self.store.add_service_graph(service_graph)

        self.assertEqual(1, self.store.all_service_graphs().count)

    def test_component_by_cnid(self):
        service_graph = ServiceGraph(nodes=[Node("my_sql", "mysql")])
        self.store.add_service_graph(service_graph)

        node = self.store.component_with_cnid("mysql")

        self.assertEqual(node.cnid, "mysql")
