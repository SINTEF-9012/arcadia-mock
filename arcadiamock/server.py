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
from sys import argv, stdout, exit

from arcadiamock import __VERSION__, __SERVICE_NAME__, __LICENSE__
from arcadiamock.utils import on_exit
from arcadiamock.servicegraphs import Store, ServiceGraph, Node
from arcadiamock.adapters import MimeTypes, XMLPrinter, TextPrinter


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
                            help='The name of the host which should serve arcadia mocks')
        parser.add_argument('-l','--log-file',
                            help='The name of the log file to use')
        parser.add_argument('-p','--port',
                            help='The port number on which HTTP requests are expected')
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

    def __init__(self, store):
        self._writers = {
            MimeTypes.XML: XMLPrinter(),
            MimeTypes.JSON: "{ \"servicegraphs\": [] }"
        }
        self._store = store
        self._store.add_service_graph(ServiceGraph(nodes=[Node(12, "foo")]))

    def about(self):
        about = self._store.about()
        return about.accept(self._writer()).as_text()

    def service_graphs(self):
        service_graphs = self._store.all_service_graphs()
        return service_graphs[0].accept(self._writer()).as_text()

    def _writer(self):
        return self._writers.get(request.accept_mimetypes.best,
                                 self._writers[MimeTypes.JSON])

    def start(self, host, port):
        app = Flask(__SERVICE_NAME__)
        app.add_url_rule('/about', 'index', self.about)
        app.add_url_rule('/service_graphs', 'service_graphs', self.service_graphs)
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

    def stop_server(self, signal, frame):
        # Let the process terminate properly, which in turn, allows
        # coverage data to be writtem to disk.
        print "Ctrl+C pressed! That's all folks!"
        stdout.flush()
        exit()


def main():
    settings = Settings.from_command_line(argv[1:])

    cli = CLI(settings, stdout)
    if settings.action == Action.SHOW_VERSION:
        cli.show_version()

    else:
        # Set up handlers for Ctrl+C and other termination signals
        on_exit(cli.stop_server)
        cli.start_server()

