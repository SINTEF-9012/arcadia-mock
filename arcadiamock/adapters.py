#
# ARCADIA Mocks
#
# Copyright (C) 2017 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#


from arcadiamock.servicegraphs import Visitor, Node, Policy, ServiceGraph, About

import xml.etree.ElementTree as etree


class MimeTypes(object):
    JSON = "application/json"
    XML = "application/xml"


class XMLNode(object):

    def __init__(self, node):
        super(XMLNode, self).__init__()
        self._root = node

    def as_text(self):
        return etree.tostring(self._root, method="xml")


class XMLPrinter(Visitor):

    def visit_service_graph_list(self, graphs):
        root = etree.Element("ServiceGraphs")
        for each_graph in graphs:
            root.append(each_graph.accept(self)._root)
        return XMLNode(root)

    def visit_about(self, name, version, license):
        root = etree.Element("about")
        name_node = etree.SubElement(root, "name")
        name_node.text = name
        version_node = etree.SubElement(root, "version")
        version_node.text = version
        license_node = etree.SubElement(root, "license")
        license_node.text = license
        return XMLNode(root)

    def visit_service_graph(self, nodes, policy, metadata):
        root =  etree.Element("ServiceGraph")
        descriptors = etree.SubElement(root, "GraphNodeDescriptor")
        for each_node in nodes:
            descriptors.append(each_node.accept(self)._root)
        return XMLNode(root)

    def visit_node(self, nid, cnid):
        root = etree.Element("GraphNode")
        nid_node = etree.SubElement(root, "NID")
        nid_node.text = str(nid)
        cnid_node = etree.SubElement(root, "CNID")
        cnid_node.text = str(cnid)
        return XMLNode(root)


class XMLParser(object):

    def about_from(self, text):
        node = etree.fromstring(text)
        return self._about_from_xml(node)

    @staticmethod
    def _about_from_xml(node):
        name = node.find("name").text
        version = node.find("version").text
        license = node.find("license").text
        return About(name, version, license)

    def graph_node_from(self, text):
        node = etree.fromstring(text)
        return self._node_from_xml(node)

    @staticmethod
    def _node_from_xml(node):
        nid = node.find("NID").text
        cnid = node.find("CNID").text
        return Node(nid, cnid);

    def runtime_policy_from(self, text):
        policy = etree.fromstring(text)
        return self._policy_from_xml(policy)

    @staticmethod
    def _policy_from_xml(policy):
        rpid = policy.find("RPID").text
        name = policy.find("RPName").text
        return Policy(rpid, name)

    def service_graph_from(self, text):
        service_graph = etree.fromstring(text)

        nodes = []
        for each_node in service_graph.find("GraphNodeDescriptor") or []:
            nodes.append(self._node_from_xml(each_node))

        policies = []
        for each_policy in service_graph.find("RuntimePolicyDescriptor") or []:
            policies.append(self._policy_from_xml(each_policy))

        return ServiceGraph(nodes, policies)

    def _service_graph_from_xml(self, node):
        nodes = []
        for each_node in node.find("GraphNodeDescriptor") or []:
            nodes.append(self._node_from_xml(each_node))

        policies = []
        for each_policy in node.find("RuntimePolicyDescriptor") or []:
            policies.append(self._policy_from_xml(each_policy))

        return ServiceGraph(nodes, policies)

    def service_graphs_from(self, text):
        collection = etree.fromstring(text)

        graphs = []
        for each_node in collection.iter("ServiceGraph") or []:
            graphs.append(self._service_graph_from_xml(each_node))

        return graphs


class TextPrinter(Visitor):
    """
    Format domain objects in raw text, which can be displayed on the
    console for instance.
    """

    ABOUT = """
    {service} v{version} -- {license}
    Copyright (C) SINTEF 2017
    """

    def visit_about(self, name, version, license):
        return self.ABOUT.format(service=name,
                                 version=version,
                                 license=license)

