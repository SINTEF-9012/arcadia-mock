#
# ARCADIA Mocks
#
# Copyright (C) 2017 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#


from arcadiamock import __VERSION__, __SERVICE_NAME__, __LICENSE__


class Store(object):

    def __init__(self):
        self._service_graphs = []

    @staticmethod
    def about():
        return About(
            __SERVICE_NAME__,
            __VERSION__,
            __LICENSE__)

    def add_service_graph(self, service_graph):
        self._service_graphs.append(service_graph)

    def all_service_graphs(self):
        return ServiceGraphList(self._service_graphs)

    def component_with_cnid(self, cnid):
        for each_graph in self._service_graphs:
            for any_node in each_graph.nodes:
                if any_node.cnid == cnid:
                    return any_node
        return None


class Visitor(object):

    def visit_about(self, name, version, code_license):
        pass

    def visit_service_graph(self, nodes, policy, metadata):
        pass

    def visit_service_graph_list(self, graphs):
        pass

    def visit_node(self, nid, cnid):
        pass

    def visit_metadata(self, values):
        pass


class DomainObject(object):
    """
    Capabilities required for all domain object (i.e., being visitable).
    """

    def accept(self, visitor):
        pass


class About(DomainObject):

    def __init__(self, name, version, code_license):
        super(About, self).__init__()
        self._name = name
        self._version = version
        self._code_license = code_license

    def accept(self, visitor):
        return visitor.visit_about(
            self._name,
            self._version,
            self._code_license)

    @property
    def name(self):
        return self._name

    @property
    def version(self):
        return self._version

    @property
    def code_license(self):
        return self._code_license


class ServiceGraphList(DomainObject):

    def __init__(self, graphs):
        self._graphs = graphs

    def accept(self, visitor):
        return visitor.visit_service_graph_list(self._graphs)

    @property
    def count(self):
        return len(self._graphs)

    @property
    def graphs(self):
        return self._graphs


class ServiceGraph(object):

    DEFAULT_IDENTIFIER = "Anonymous"

    def __init__(self, identifier=None, nodes=None, policy=None, metadata=None):
        self._identifier = identifier or self.DEFAULT_IDENTIFIER
        self._nodes = nodes or []
        self._policy = policy
        self._metadata = metadata

    def accept(self, visitor):
        return visitor.visit_service_graph(
            self._nodes,
            self._policy,
            self._metadata)

    @property
    def identifier(self):
        return self._identifier

    @property
    def nodes(self):
        return self._nodes

    def add_node(self, node):
        self._nodes.append(node)

    @property
    def policy(self):
        return self._policy

    @policy.setter
    def policy(self, policy):
        self._policy = policy

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        self._metadata = metadata


class Node(object):

    DEFAULT_ID = "Unknown"
    DEFAULT_CNID = "Unknown"

    def __init__(self, nid=None, cnid=None):
        self._nid = nid or Node.DEFAULT_ID
        self._cnid = cnid or Node.DEFAULT_CNID

    def accept(self, visitor):
        return visitor.visit_node(self.nid, self.cnid)

    @property
    def nid(self):
        return self._nid

    @property
    def cnid(self):
        return self._cnid


class Policy(object):

    DEFAULT_ID = "Unknown"
    DEFAULT_NAME = "Anonymous"

    def __init__(self, rpid=None, name=None):
        self._rpid = rpid or Policy.DEFAULT_ID
        self._name = name or Policy.DEFAULT_NAME

    @property
    def rpid(self):
        return self._rpid

    @property
    def name(self):
        return self._name


class MetaData(DomainObject):

    def __init__(self, values = {}):
        self._values = values

    def bind(self, key, value):
        self._values[key] = value

    def value_of(self, key):
        return self._values.get(key, None)

    def accept(self, visitor):
        return visitor.visit_metadata(self._values)

    @property
    def count(self):
        return len(self._values)
