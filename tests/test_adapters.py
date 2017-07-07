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

from arcadiamock.servicegraphs import ServiceGraph, Component, Node, About, MetaData, ComponentList
from arcadiamock.adapters import XMLPrinter, XMLParser


class XMLParserTests(TestCase):

    def setUp(self):
        self.parser = XMLParser()

    def test_parse_graph_node(self):
        xml = """
        <GraphNode>
        <NID>graph_node_mysql_id</NID>
        <CNID>mysql_id</CNID>
        </GraphNode>
        """

        node = self.parser.graph_node_from(xml)

        self.assertIsNotNone(node)
        self.assertEquals("graph_node_mysql_id", node.nid)
        self.assertEquals("mysql_id", node.cnid)

    def test_parse_runtime_policy(self):
        xml = """
        <RuntimePolicy>
        <RPID>RPID</RPID>
        <RPName>RPName</RPName>
        </RuntimePolicy>
        """

        policy = self.parser.runtime_policy_from(xml)

        self.assertIsNotNone(policy)
        self.assertEqual("RPID", policy.rpid)
        self.assertEqual("RPName", policy.name)

    def test_parse_service_graph(self):
        xml = """
        <ServiceGraph xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="ArcadiaModellingArtefacts.xsd">
        <DescriptiveSGMetadata>
            <SGID>wordpress_mysql_service_graph_id</SGID>
            <SGName>SimpleWordPressServiceGraph</SGName>
            <SGDescription>SGDescription</SGDescription>
        </DescriptiveSGMetadata>
        <GraphNodeDescriptor>
            <GraphNode>
                <NID>graph_node_mysql_id</NID>
                <CNID>mysql_id</CNID>
            </GraphNode>
            <GraphNode>
                <NID>graph_node_wordpress_id</NID>
                <CNID>wordpress_id</CNID>
                <GraphDependency>
                    <CEPCID>mysqltcp_cepcid</CEPCID>
                    <ECEPID>mysqltcp</ECEPID>
                    <NID>NID</NID>
                </GraphDependency>
            </GraphNode>
        </GraphNodeDescriptor>
        <RuntimePolicyDescriptor>
            <RuntimePolicy>
                <RPID>RPID</RPID>
                <RPName>RPName</RPName>
           </RuntimePolicy>
        </RuntimePolicyDescriptor>
     </ServiceGraph>
        """

        service_graph = self.parser.service_graph_from(xml)

        self.assertIsNotNone(service_graph)
        self.assertEqual(2, len(service_graph.nodes))

    def test_parse_service_graphs(self):
        xml = "<ServiceGraphs>"\
              "<ServiceGraph />"\
              "<ServiceGraph />"\
              "</ServiceGraphs>"

        service_graphs = self.parser.service_graphs_from(xml)

        self.assertEqual(2, len(service_graphs))

    def test_parse_metadata(self):
        xml = "<DescriptiveSGMetadata>" \
              "<FOO>foo value</FOO>"\
              "<BAR>bar value</BAR>"\
              "</DescriptiveSGMetadata>"

        metadata = self.parser.metadata_from(xml)

        self.assertEqual(metadata.count, 2)
        self.assertEqual("foo value", metadata.value_of("FOO"))
        self.assertEqual("bar value", metadata.value_of("BAR"))

    def test_parse_component(self):
        xml = "<Component>"\
              "<CID>1</CID>"\
              "<CNID>2</CNID>"\
              "<CEPNID>3</CEPNID>"\
              "<ECEPCNID>4</ECEPCNID>"\
              "</Component>"

        component = self.parser.component_from(xml)

        self.assertEqual("1", component.cid)
        self.assertEqual("2", component.cnid)
        self.assertEqual("3", component.cepnid)
        self.assertEqual("4", component.ecepcnid)

    def test_parse_component_list(self):
        xml = "<Components>"\
              "<Component>"\
              "<CID>1</CID>"\
              "<CNID>2</CNID>"\
              "<CEPNID>3</CEPNID>"\
              "<ECEPCNID>4</ECEPCNID>"\
              "</Component>"\
              "</Components>"

        components = self.parser.components_from(xml)

        self.assertEqual(1, components.count)


class XMLPrinterTests(TestCase):

    def setUp(self):
        self.printer = XMLPrinter()

    def test_printing_about_information(self):
        about = About("foo", "1.3.2", "MIT")

        xml = about.accept(self.printer)

        expected_xml = "<about>"\
                       "<name>foo</name>" \
                       "<version>1.3.2</version>" \
                       "<license>MIT</license>" \
                       "</about>"
        self.assertEqual(expected_xml, xml.as_text())

    def test_printing_service_graph(self):
        service_graph = ServiceGraph(
            nodes= [ Node(23, "foo"),
                     Node(24, "bar") ],
            metadata = MetaData({"foo": "bar"}))

        xml = service_graph.accept(self.printer)

        expected = "<ServiceGraph>"\
                   "<DescriptiveSGMetadata>" \
                   "<FOO>bar</FOO>"\
                   "</DescriptiveSGMetadata>"\
                   "<GraphNodeDescriptor>"\
                   "<GraphNode>"\
                   "<NID>23</NID>"\
                   "<CNID>foo</CNID>"\
                   "</GraphNode>"\
                   "<GraphNode>"\
                   "<NID>24</NID>"\
                   "<CNID>bar</CNID>"\
                   "</GraphNode>"\
                   "</GraphNodeDescriptor>"\
                   "</ServiceGraph>"
        self.assertEquals(expected, xml.as_text())

    def test_printing_node(self):
        node = Node(23, "foo")

        xml = node.accept(self.printer)

        expected = "<GraphNode>"\
                   "<NID>23</NID>"\
                   "<CNID>foo</CNID>"\
                   "</GraphNode>"
        self.assertEqual(expected, xml.as_text())

    def test_printing_metadata(self):
        metadata = MetaData({"foo": "bar"})

        xml = metadata.accept(self.printer)

        expected = "<DescriptiveSGMetadata>" \
                   "<FOO>bar</FOO>"\
                   "</DescriptiveSGMetadata>"
        self.assertEquals(expected, xml.as_text())

    def test_printing_component(self):
        component = Component(
            cid=1,
            cnid=2,
            cepnid=3,
            ecepcnid=4)

        xml = component.accept(self.printer)

        expected = "<Component>"\
                   "<CID>1</CID>"\
                   "<CNID>2</CNID>"\
                   "<CEPNID>3</CEPNID>"\
                   "<ECEPCNID>4</ECEPCNID>"\
                   "</Component>"
        self.assertEqual(expected, xml.as_text())

    def test_printing_empty_component_list(self):
        components = ComponentList()

        xml = components.accept(self.printer)

        expected = "<Components/>"

        self.assertEqual(expected, xml.as_text())

    def test_printing_empty_component_list(self):
        components = ComponentList([ Component() ])

        xml = components.accept(self.printer)

        expected = "<Components>"\
                   "<Component>"\
                   "<CID>0</CID>"\
                   "<CNID>0</CNID>"\
                   "<CEPNID>0</CEPNID>"\
                   "<ECEPCNID>0</ECEPCNID>"\
                   "</Component>"\
                   "</Components>"
        self.assertEqual(expected, xml.as_text())

