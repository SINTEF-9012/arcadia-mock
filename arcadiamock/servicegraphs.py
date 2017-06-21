#
# ARCADIA Mocks
#
# Copyright (C) 2017 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#


class Store(object):

    def __init__(self):
        self._service_graphs = []

    def add_service_graph(self, service_graph):
        self._service_graphs.append(service_graph)

    def all_service_graphs(self):
        return self._service_graphs


class Visitor(object):

    def visit_service_graph(self, nodes, policy, metadata):
        pass

    def visit_node(nid, cnid):
        pass


class ServiceGraph(object):

    def __init__(self, nodes=None, policy=None):
        self._nodes = nodes or []
        self._policy = policy
        self._metadata = None

    def accept(self, visitor):
        return visitor.visit_service_graph(
            self._nodes,
            self._policy,
            self._metadata)

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


class MetaData(object):
    pass


