#
# ARCADIA Mocks
#
# Copyright (C) 2017 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#

from subprocess import Popen
from sys import platform


def on_exit(handler):
    if platform == "win32":
        from signal import signal, SIGBREAK
        signal(SIGBREAK, handler)
    else:
        from signal import signal, SIGTERM
        signal(SIGTERM, handler)
 

def spawn(command_line, log_file=None):
    if platform == "win32":
        from subprocess import CREATE_NEW_PROCESS_GROUP
        process = Popen(command_line, 
                        stdout=log_file, 
                        stderr=log_file, 
                        creationflags=CREATE_NEW_PROCESS_GROUP)
        return Win32Process(process)
    process = Popen(command_line, 
                    stdout=log_file, 
                    stderr=log_file)
    return PosixProcess(process)


class AbstractProcess(object):

    def __init__(self, process):
        self._process = process

    def poll(self):
        return self._process.poll()

    def terminate(self):
        pass


class PosixProcess(AbstractProcess):

    def __init__(self, process):
        super(PosixProcess, self).__init__(process)

    def terminate(self):
        from signal import SIGTERM
        self._process.send_signal(SIGTERM)


class Win32Process(AbstractProcess):

    def __init__(self, process):
        super(Win32Process, self).__init__(process)

    def terminate(self):
        from signal import CTRL_BREAK_EVENT
        self._process.send_signal(CTRL_BREAK_EVENT)

