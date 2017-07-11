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

    def __init__(self, service_graphs=[], components=[]):
        self._service_graphs = service_graphs
        self._components = ComponentList(components)

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

    def all_components(self):
        return self._components

    def register_component(self, component):
        self._components.add(component)

    def component_with_cnid(self, cnid):
        return self._components.with_cnid(cnid)


class Visitor(object):

    def visit_about(self, name, version, code_license):
        pass

    def visit_service_graph(self, nodes, policy, metadata):
        pass

    def visit_service_graph_list(self, graphs):
        pass

    def visit_node(self, nid, cnid, dependency):
        pass

    def visit_metadata(self, values):
        pass

    def visit_dependency(self, nid, cepcid, ecepid):
        pass


class DomainObject(object):
    """
    Capabilities required for all domain objects (i.e., being visitable).
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


class Component(DomainObject):

    DEFAULT_CID = None
    DEFAULT_CNID = None
    DEFAULT_CEPNID = None
    DEFAULT_ECEPCNID = None

    def __init__(self, cid=None, cnid=None, cepnid=None, ecepcnid=None):
        self._cnid = cnid or self.DEFAULT_CNID
        self._cid = cid or self.DEFAULT_CID
        self._cepnid = cepnid or self.DEFAULT_CEPNID
        self._ecepcnid = ecepcnid or self.DEFAULT_ECEPCNID

    def accept(self, visitor):
        return visitor.visit_component(
            self.cid,
            self.cnid,
            self.cepnid,
            self.ecepcnid)

    @property
    def cnid(self):
        return self._cnid

    @property
    def cid(self):
        return self._cid

    @property
    def cepnid(self):
        return self._cepnid

    @property
    def ecepcnid(self):
        return self._ecepcnid


class ComponentList(DomainObject):

    def __init__(self, components=[]):
        self._components = components

    @property
    def count(self):
        return len(self._components)

    def accept(self, visitor):
        return visitor.visit_component_list(self._components)

    def with_cnid(self, cnid):
        for any_component in self._components:
            if any_component.cnid == cnid:
                return any_component
        return None

    def add(self, component):
        self._components.append(component)

    def __getitem__(self, key):
        return self._components[key]


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

    def __init__(self, nid=None, cnid=None, dependency=None):
        self._nid = nid or Node.DEFAULT_ID
        self._cnid = cnid or Node.DEFAULT_CNID
        self._dependency = dependency

    def accept(self, visitor):
        return visitor.visit_node(self.nid, self.cnid, self.dependency)

    @property
    def nid(self):
        return self._nid

    @property
    def cnid(self):
        return self._cnid

    @property
    def dependency(self):
        return self._dependency


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


class Dependency(DomainObject):

    def __init__(self, nid=None, cepcid=None, ecepid=None):
        self._nid = nid
        self._cepcid = cepcid
        self._ecepid = ecepid

    def accept(self, visitor):
        return visitor.visit_dependency(self.nid,
                                        self.cepcid,
                                        self.ecepid)

    @property
    def nid(self):
        return self._nid

    @property
    def cepcid(self):
        return self._cepcid

    @property
    def ecepid(self):
        return self._ecepid
