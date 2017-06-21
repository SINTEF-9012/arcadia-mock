#
# ARCADIA Mocks
#
# Copyright (C) 2017 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#


from arcadiamock.servicegraphs import Visitor, Node, Policy, ServiceGraph

import xml.etree.ElementTree as etree


class XMLNode(object):

    def __init__(self, node):
        super(XMLNode, self).__init__()
        self._root = node

    def as_text(self):
        return etree.tostring(self._root, method="xml")


class XMLPrinter(Visitor):

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

    def graph_node_from(self, text):
        node = etree.fromstring(text)
        return self._node_from_xml(node)
    
    def _node_from_xml(self, node):
        nid = node.find("NID").text
        cnid = node.find("CNID").text
        return Node(nid, cnid);

    def runtime_policy_from(self, text):
        policy = etree.fromstring(text)
        return self._policy_from_xml(policy)

    def _policy_from_xml(self, policy):
        rpid = policy.find("RPID").text
        name = policy.find("RPName").text
        return Policy(rpid, name)

    def service_graph_from(self, text):
        service_graph = etree.fromstring(text)
        
        nodes = []
        for each_node in service_graph.find("GraphNodeDescriptor"):
            nodes.append(self._node_from_xml(each_node))

        policies = []
        for each_policy in service_graph.find("RuntimePolicyDescriptor"):
            policies.append(self._policy_from_xml(each_policy))
            
        return ServiceGraph(nodes, policies)
            
