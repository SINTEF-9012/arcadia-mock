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
from io import StringIO

from arcadiamock import __VERSION__, __SERVICE_NAME__, __LICENSE__
from arcadiamock.server import CLI, Settings, Action
from arcadiamock.adapters import TextPrinter


class CLITests(TestCase):

    def test_show_version(self):
        output = StringIO()
        settings = Settings("127.0.0.1", 5000, output, Action.SHOW_VERSION)
        cli = CLI(settings, output)

        cli.show_version()

        expected = TextPrinter.ABOUT.format(
            version=__VERSION__,
            code_license=__LICENSE__,
            service=__SERVICE_NAME__)
        self.assertEqual(expected, output.getvalue())


class SettingsTests(TestCase):

    def test_default_action(self):
        settings = Settings.from_command_line([])
        self.assertEqual(Action.START, settings.action)

    def test_show_version_long_format(self):
        settings = Settings.from_command_line(["--version"])
        self.assertEqual(Action.SHOW_VERSION, settings.action)

    def test_show_version_short_format(self):
        settings = Settings.from_command_line(["-v"])
        self.assertEqual(Action.SHOW_VERSION, settings.action)

    def test_default_hostname(self):
        settings = Settings.from_command_line([])
        self.assertEquals(Settings.DEFAULT_HOSTNAME, settings.hostname)

    def test_default_hostname_long_format(self):
        hostname = "127.0.0.1"
        settings = Settings.from_command_line(["--name", hostname])
        self.assertEquals(hostname, settings.hostname)

    def test_default_hostname_short_format(self):
        hostname = "127.0.0.1"
        settings = Settings.from_command_line(["-n", hostname])
        self.assertEquals(hostname, settings.hostname)

    def test_default_port_number(self):
        settings = Settings.from_command_line([])
        self.assertEqual(int(Settings.DEFAULT_PORT), settings.port)

    def test_parsing_port_number_long_format(self):
        port = "1234"
        settings = Settings.from_command_line(["--port", port])
        self.assertEqual(int(port), settings.port)

    def test_parsing_port_number_short_format(self):
        port = "1234"
        settings = Settings.from_command_line(["-p", port])
        self.assertEqual(int(port), settings.port)

    def test_default_log_file_name(self):
        settings = Settings.from_command_line([])
        self.assertEqual(Settings.DEFAULT_LOG_FILE, settings.log_file)

    def test_parsing_log_file_name_long_format(self):
        log_file = "my_log_file.log"
        settings = Settings.from_command_line(["--log-file", log_file])
        self.assertEqual(log_file, settings.log_file)

    def test_parsing_log_file_name_short_format(self):
        log_file = "my_log_file.log"
        settings = Settings.from_command_line(["-l", log_file])
        self.assertEqual(log_file, settings.log_file)

