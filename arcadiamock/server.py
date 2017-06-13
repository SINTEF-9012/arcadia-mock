#
# ARCADIA Mocks
#
# Copyright (C) 2017 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#


from flask import Flask
from argparse import ArgumentParser
from sys import argv, stdout

from arcadiamock import __VERSION__, __SERVICE_NAME__, __LICENSE__


class Action:
    SHOW_VERSION = 1,
    START = 2


class Settings:
    """
    Contains the options/arguments given on the command line.
    """

    DEFAULT_ACTION = Action.START
    DEFAULT_LOG_FILE = "arcadiamock.log"
    DEFAULT_PORT = "8080"

    @staticmethod
    def from_command_line(arguments):
        parser = ArgumentParser(description='ARCADIA Mock')
        parser.add_argument('--version', "-v", 
                            action="store_const",
                            dest="action",
                            const=Action.SHOW_VERSION,
                            help='show the version')
        parser.add_argument('-l','--log-file', 
                            help='The name of the log file to use')
        parser.add_argument('-p','--port', 
                            help='The port number on which HTTP requests are expected')
        parser.set_defaults(
            action=Settings.DEFAULT_ACTION,
            log_file=Settings.DEFAULT_LOG_FILE,
            port=Settings.DEFAULT_PORT
        )
        
        values = parser.parse_args(arguments)
        return Settings(int(values.port), values.log_file, values.action)

    def __init__(self, port, log_file, action):
        self._port = port 
        self._log_file = log_file
        self._action = action
        
    @property
    def action(self):
        return self._action

    @property
    def log_file(self):
        return self._log_file

    @property
    def port(self):
        return self._port


class ArcadiaMocks:
    """
    Facade class that offers all functionalities available from the
    command line (e.g., show_version, start).
    """

    ABOUT = """
    {service} v{version} -- {license}
    Copyright (C) SINTEF 2017
    """

    def __init__(self, output):
        self._output = output
    
    def show_version(self):
        self._output.write(unicode(self.version()))

    def version(self):
        return ArcadiaMocks.ABOUT.format(
            version=__VERSION__,
            service=__SERVICE_NAME__,
            license=__LICENSE__)

    def start(self):
        app = Flask(__SERVICE_NAME__)
        app.add_url_rule('/about', 'index', self.version)
        app.run()

def main():
    stdout.flush()
    settings = Settings.from_command_line(argv[1:])
    mocks = ArcadiaMocks(stdout)
    if settings.action == Action.START:
        mocks.start()
    elif settings.action == Action.SHOW_VERSION:
        mocks.show_version()
    else:
        print("Unsupported command!")
        

if __name__ == "__main__":
    main()
