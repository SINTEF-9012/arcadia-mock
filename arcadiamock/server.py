#
# ARCADIA Mocks
#
# Copyright (C) 2017 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#


from flask import Flask, request
from argparse import ArgumentParser
from sys import argv, stdout, exit as sys_exit

from arcadiamock import __SERVICE_NAME__
from arcadiamock.utils import on_exit
from arcadiamock.servicegraphs import Store, ServiceGraph, Node, Component
from arcadiamock.adapters import MimeTypes, XMLPrinter, HTMLPrinter, XMLParser, TextPrinter


class Action(object):
    SHOW_VERSION = 1,
    START = 2


class Settings(object):
    """
    Contains the options/arguments given on the command line.
    """

    DEFAULT_ACTION = Action.START
    DEFAULT_LOG_FILE = "arcadiamock.log"
    DEFAULT_HOSTNAME = "127.0.0.1"
    DEFAULT_PORT = "8080"

    @staticmethod
    def from_command_line(arguments):
        parser = ArgumentParser(description='ARCADIA Mock')
        parser.add_argument('--version', "-v",
                            action="store_const",
                            dest="action",
                            const=Action.SHOW_VERSION,
                            help='show the version')
        parser.add_argument('-n','--name',
                            help="The name of the host which should serve arcadia mocks")
        parser.add_argument('-l','--log-file',
                            help='The name of the log file to use')
        parser.add_argument('-p','--port',
                            help="The port number on which HTTP requests are expected")
        parser.set_defaults(
            action=Settings.DEFAULT_ACTION,
            log_file=Settings.DEFAULT_LOG_FILE,
            port=Settings.DEFAULT_PORT,
            name=Settings.DEFAULT_HOSTNAME
        )

        values = parser.parse_args(arguments)
        return Settings(values.name,
                        int(values.port),
                        values.log_file,
                        values.action)

    def __init__(self, hostname, port, log_file, action):
        self._hostname = hostname
        self._port = port
        self._log_file = log_file
        self._action = action

    @property
    def hostname(self):
        return self._hostname

    @property
    def action(self):
        return self._action

    @property
    def log_file(self):
        return self._log_file

    @property
    def port(self):
        return self._port


class RESTServer(object):

    DEFAULT_COMPONENTS = [
        Component(cid="1234", cnid="mysql_id", cepnid=None, ecepcnid=None),
        Component(cid="2345", cnid="wordpress_id", cepnid=None, ecepcnid=None)
    ]

    def __init__(self, store):
        self._writers = {
            MimeTypes.XML: XMLPrinter(),
            MimeTypes.HTML : HTMLPrinter(),
            MimeTypes.JSON: "{ \"servicegraphs\": [] }"
        }
        self._store = store
        for each_component in self.DEFAULT_COMPONENTS:
            self._store.register_component(each_component)

    def about(self):
        about = self._store.about()
        return about.accept(self._writer()).as_text()

    def service_graphs(self):
        service_graphs = self._store.all_service_graphs()
        return service_graphs.accept(self._writer()).as_text()

    def register_service_graph(self):
        service_graph = XMLParser().service_graph_from(request.data)
        self._store.add_service_graph(service_graph)
        return ("", 200)

    def components(self):
        components = self._store.all_components()
        return components.accept(self._writer()).as_text()

    def register_component(self):
        component = XMLParser().component_from(request.data)
        self._store.register_component(component)
        return ("", 200)

    def component_with_cnid(self, cnid):
        print "Searching for CNID '", cnid, "'"
        component = self._store.component_with_cnid(cnid)
        if component is None:
            return ("Not Found", 404)
        return component.accept(self._writer()).as_text()

    def _writer(self):
        return self._writers.get(request.accept_mimetypes.best,
                                 self._writers[MimeTypes.JSON])

    def start(self, host, port):
        app = Flask(__SERVICE_NAME__)
        app.add_url_rule('/about',
                         view_func=self.about)
        app.add_url_rule('/service_graphs',
                         view_func=self.service_graphs)
        app.add_url_rule("/register",
                         methods=["POST"],
                         view_func=self.register_service_graph)
        app.add_url_rule("/components",
                         view_func=self.components)
        app.add_url_rule("/components",
                         methods=["POST"],
                         view_func=self.register_component)
        app.add_url_rule("/components/<cnid>",
                         view_func=self.component_with_cnid)
        app.run(host=host, port=port)


class CLI(object):

    def __init__(self, settings, output):
        self._settings = settings
        self._output = output
        self._store = Store()

    def show_version(self):
        about = self._store.about()
        self._output.write(unicode(about.accept(TextPrinter())))

    def start_server(self):
        server = RESTServer(self._store)
        server.start(host=self._settings.hostname,
                     port=self._settings.port)

    @staticmethod
    def stop_server(signal, frame):
        # Let the process terminate properly, which in turn, allows
        # coverage data to be writtem to disk.
        print "Ctrl+C pressed! That's all folks!"
        stdout.flush()
        sys_exit()


def main():
    settings = Settings.from_command_line(argv[1:])

    cli = CLI(settings, stdout)

    if settings.action == Action.SHOW_VERSION:
        cli.show_version()

    else:
        # Set up handlers for Ctrl+C and other termination signals
        on_exit(cli.stop_server)
        cli.start_server()

