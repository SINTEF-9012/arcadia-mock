#
# ARCADIA Mocks
#
# Copyright (C) 2017 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#


from arcadiamock.servicegraphs import *

import xml.etree.ElementTree as etree
from lxml import etree as lxmletree


class MimeTypes(object):
    JSON = "application/json"
    XML = "application/xml"
    HTML = "text/html"


class XMLNode(object):

    def __init__(self, node):
        super(XMLNode, self).__init__()
        self._root = node

    def as_text(self):
        return etree.tostring(self._root, method="xml")


class HTMLNode(object):

    def __init__(self, node):
        super(HTMLNode, self).__init__()
        self._root = node

    def as_text(self):
        root = lxmletree.fromstring(etree.tostring(self._root))
        return lxmletree.tostring(root, pretty_print=True)


class HTMLPrinter(Visitor):

    def visit_component_list(self, components):
        group = etree.Element("Components")
        for each_component in components:
            group.append(each_component.accept(self)._root)
        return HTMLNode(group)

    def visit_component(self, cid, cnid, cepnid, ecepcnid):
        component = etree.Element("Component")
        self._append_node(component, "NID", cid)
        self._append_node(component, "CNID", cnid)
        self._append_node(component, "CEPCID", cepnid)
        self._append_node(component, "ECEPID", ecepcnid)
        return HTMLNode(component)

    def visit_service_graph_list(self, graphs):
        root = etree.Element("ServiceGraphs")
        for each_graph in graphs:
            root.append(each_graph.accept(self)._root)
        return HTMLNode(root)

    def visit_about(self, name, version, code_license):
        root = etree.Element("about")
        self._append_node(root, "name", name)
        self._append_node(root, "version", version)
        self._append_node(root, "license", code_license)
        return HTMLNode(root)

    def visit_service_graph(self, nodes, policy, metadata):
        attributes = dict()
        attributes['xmlns:xsi'] = 'http://www.w3.org/2001/XMLSchema-instance'
        attributes['xsi:noNamespaceSchemaLocation'] = 'ArcadiaModellingArtefacts.xsd'
        root =  etree.Element("ServiceGraph", attrib = attributes)
        if metadata is not None:
            root.append(metadata.accept(self)._root)
        descriptors = etree.SubElement(root, "GraphNodeDescriptor")
        for each_node in nodes:
            descriptors.append(each_node.accept(self)._root)
        return HTMLNode(root)

    def visit_node(self, nid, cnid, dependency):
        root = etree.Element("GraphNode")
        self._append_node(root, "NID", nid)
        self._append_node(root, "CNID", cnid)
        if dependency is not None:
            root.append(dependency.accept(self)._root)
        return HTMLNode(root)

    def visit_dependency(self, nid, cepcid, ecepid):
        dependency = etree.Element("GraphDependency")
        self._append_node(dependency, "NID", nid)
        self._append_node(dependency, "CEPCID", cepcid)
        self._append_node(dependency, "ECEPID", ecepid)
        return HTMLNode(dependency)

    def visit_metadata(self, values):
        root = etree.Element("DescriptiveSGMetadata")
        for key, value in values.items():
            node = etree.SubElement(root, key.upper())
            node.text = value
        return HTMLNode(root)

    @staticmethod
    def _append_node(root, name, text):
        if text is not None:
            node = etree.SubElement(root, name)
            node.text = str(text)


class XMLPrinter(Visitor):

    def visit_component_list(self, components):
        group = etree.Element("Components")
        for each_component in components:
            group.append(each_component.accept(self)._root)
        return XMLNode(group)

    def visit_component(self, cid, cnid, cepnid, ecepcnid):
        component = etree.Element("Component")
        self._append_node(component, "NID", cid)
        self._append_node(component, "CNID", cnid)
        self._append_node(component, "CEPCID", cepnid)
        self._append_node(component, "ECEPID", ecepcnid)
        return XMLNode(component)

    def visit_service_graph_list(self, graphs):
        root = etree.Element("ServiceGraphs")
        for each_graph in graphs:
            root.append(each_graph.accept(self)._root)
        return XMLNode(root)

    def visit_about(self, name, version, code_license):
        root = etree.Element("about")
        self._append_node(root, "name", name)
        self._append_node(root, "version", version)
        self._append_node(root, "license", code_license)
        return XMLNode(root)

    def visit_service_graph(self, nodes, policy, metadata):
        root =  etree.Element("ServiceGraph")
        if metadata is not None:
            root.append(metadata.accept(self)._root)
        descriptors = etree.SubElement(root, "GraphNodeDescriptor")
        for each_node in nodes:
            descriptors.append(each_node.accept(self)._root)
        return XMLNode(root)

    def visit_node(self, nid, cnid, dependency):
        root = etree.Element("GraphNode")
        self._append_node(root, "NID", nid)
        self._append_node(root, "CNID", cnid)
        if dependency is not None:
            root.append(dependency.accept(self)._root)
        return XMLNode(root)

    def visit_dependency(self, nid, cepcid, ecepid):
        dependency = etree.Element("GraphDependency")
        self._append_node(dependency, "NID", nid)
        self._append_node(dependency, "CEPCID", cepcid)
        self._append_node(dependency, "ECEPID", ecepid)
        return XMLNode(dependency)

    def visit_metadata(self, values):
        root = etree.Element("DescriptiveSGMetadata")
        for key, value in values.items():
            node = etree.SubElement(root, key.upper())
            node.text = value
        return XMLNode(root)

    @staticmethod
    def _append_node(root, name, text):
        if text is not None:
            node = etree.SubElement(root, name)
            node.text = str(text)


class XMLParser(object):

    def about_from(self, text):
        node = etree.fromstring(text)
        return self._about_from_xml(node)

    @staticmethod
    def _about_from_xml(node):
        name = node.find("name").text
        version = node.find("version").text
        code_license = node.find("license").text
        return About(name, version, code_license)

    @classmethod
    def _fetch_attribute(cls, node, attribute):
        return node.find(attribute).text if node.find(attribute) is not None else None

    def graph_node_from(self, text):
        node = etree.fromstring(text)
        return self._node_from_xml(node)

    @classmethod
    def _node_from_xml(cls, node):
        nid = cls._fetch_attribute(node, "NID")
        cnid = cls._fetch_attribute(node, "CNID")
        dependency = node.find("GraphDependency")
        if dependency is not None:
            dependency = XMLParser._dependency_from_xml(dependency)
        return Node(nid, cnid, dependency);

    def dependency_from(self, text):
        dependency = etree.fromstring(text)
        return self._dependency_from_xml(dependency)

    @classmethod
    def _dependency_from_xml(cls, dependency):
        nid = cls._fetch_attribute(dependency, "NID")
        cepcid = cls._fetch_attribute(dependency, "CEPCID")
        ecepid = cls._fetch_attribute(dependency, "ECEPID")
        return Dependency(nid, cepcid, ecepid)

    def runtime_policy_from(self, text):
        policy = etree.fromstring(text)
        return self._policy_from_xml(policy)

    @staticmethod
    def _policy_from_xml(policy):
        rpid = policy.find("RPID").text
        name = policy.find("RPName").text
        return Policy(rpid, name)

    def service_graph_from(self, text):
        node = etree.fromstring(text)
        return self._service_graph_from_xml(node)

    def _service_graph_from_xml(self, node):
        nodes = []
        for each_node in node.find("GraphNodeDescriptor") or []:
            nodes.append(self._node_from_xml(each_node))

        policies = []
        for each_policy in node.find("RuntimePolicyDescriptor") or []:
            policies.append(self._policy_from_xml(each_policy))

        return ServiceGraph(nodes=nodes, policy=policies)

    def service_graphs_from(self, text):
        collection = etree.fromstring(text)

        graphs = []
        for each_node in collection.iter("ServiceGraph") or []:
            graphs.append(self._service_graph_from_xml(each_node))

        return graphs

    def metadata_from(self, text):
        values = {}
        root = etree.fromstring(text)
        for each_node in root:
            values[each_node.tag] = each_node.text
        return MetaData(values)

    def component_from(self, text):
        node = etree.fromstring(text)
        return self._component_from_xml(node)

    @classmethod
    def _component_from_xml(cls, node):
        cid = cls._fetch_attribute(node, "NID")
        cnid = cls._fetch_attribute(node, "CNID")
        cepnid = cls._fetch_attribute(node, "CEPCID")
        ecepcnid = cls._fetch_attribute(node,"ECEPID")
        return Component(cid=cid,
                         cnid=cnid,
                         cepnid=cepnid,
                         ecepcnid=ecepcnid)

    def components_from(self, text):
        collection = etree.fromstring(text)
        components = []
        for each_component in collection.iter("Component") or []:
            components.append(self._component_from_xml(each_component))
        return ComponentList(components)


class TextPrinter(Visitor):
    """
    Format domain objects in raw text, which can be displayed on the
    console for instance.
    """

    ABOUT = """
    {service} v{version} -- {code_license}
    Copyright (C) SINTEF 2017
    """

    def visit_about(self, name, version, code_license):
        return self.ABOUT.format(service=name,
                                 version=version,
                                 code_license=code_license)

