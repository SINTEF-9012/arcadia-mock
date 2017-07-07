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

    def test_identifer(self):
        self.assertEqual(ServiceGraph.DEFAULT_IDENTIFIER, self.graph.identifier)

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


class DefaultComponentTests(TestCase):

    def setUp(self):
        self.component = Component()

    def test_default_cid(self):
        self.assertEqual(Component.DEFAULT_CID, self.component.cid)

    def test_default_cnid(self):
        self.assertEqual(Component.DEFAULT_CNID, self.component.cnid)

    def test_default_cepnid(self):
        self.assertEqual(Component.DEFAULT_CEPNID, self.component.cepnid)

    def test_default_ecepcnid(self):
        self.assertEqual(Component.DEFAULT_ECEPCNID, self.component.ecepcnid)


class CustomComponentTests(TestCase):

    def setUp(self):
        self.cid = "foo"
        self.cnid = "bar"
        self.cepnid = "baz"
        self.ecepcnid = "quz"
        self.component = Component(cid=self.cid,
                                   cnid=self.cnid,
                                   cepnid=self.cepnid,
                                   ecepcnid=self.ecepcnid)

    def test_cid(self):
        self.assertEqual(self.cid, self.component.cid)

    def test_cnid(self):
        self.assertEqual(self.cnid, self.component.cnid)

    def test_cepnid(self):
        self.assertEqual(self.cepnid, self.component.cepnid)

    def test_ecepcnid(self):
        self.assertEqual(self.ecepcnid, self.component.ecepcnid)

    def test_accept(self):
        visitor = MagicMock()
        self.component.accept(visitor)
        visitor.visit_component.assert_called_once()


class MetadataTests(TestCase):

    def setUp(self):
        self.metadata = MetaData()

    def test_defining_key_value_pair(self):
        key, value = ("foo", "foo value")

        self.metadata.bind(key, value)

        self.assertEqual(value, self.metadata.value_of(key))

    def test_accept(self):
        visitor = MagicMock()

        self.metadata.accept(visitor)

        visitor.visit_metadata.assert_called_once()


class EmptyComponentListTest(TestCase):

    def setUp(self):
        self.components = ComponentList()

    def test_count(self):
        self.assertEqual(0, self.components.count)

    def test_accept(self):
        visitor = MagicMock()
        self.components.accept(visitor)
        visitor.visit_component_list.assert_called_once()


class PrefilledStoreTests(TestCase):

    def setUp(self):
        self._components = [
            Component(cid=123,
                      cnid=1234)
            ]
        self.store = Store(components=self._components)

    def test_all_components(self):
        self.assertEqual(1, self.store.all_components().count)
        self.assertIs(self._components[0], self.store.all_components()[0])

    def test_component_by_cnid(self):
        node = self.store.component_with_cnid(1234)
        self.assertEqual(node.cnid, 1234)


class EmptyStoreTests(TestCase):

    def setUp(self):
        self.store = Store()

    def test_add_service_graphs(self):
        self.store.add_service_graph(ServiceGraph())
        self.assertEqual(1, self.store.all_service_graphs().count)

    def test_components(self):
        self.assertEquals(0, self.store.all_components().count)

    def test_component_by_cnid(self):
        self.assertIsNone(self.store.component_with_cnid(1243))

    def test_register_component(self):
        component = Component(cnid="foo")
        self.store.register_component(component)
        self.assertEqual(1, self.store.all_components().count)
