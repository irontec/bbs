# -*- coding: utf-8 -*-
# Copyright (C) 2017  Irontec S.L.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import abc
import threading
import time


class Step(object):
    """
    Abstract base class for steps.
    All step classes should be derivated from this.

    Instance attributes:
      index: int
        Position of this step in the whole scenario. This vale only affects
        secuential types scenarios.
      session: Session
        Session instance this step belongs to. Used to access session active
        calls and SIP session account.
      success: bool = None
        Determines if the step has been completed successfully. If None, the
        step has not yet runned or condition to determine success has not yet
        met.
      timeout: int = 5
        Determines how much seconds wait_status will wait before considering
        the step failed. This can be overriden by function parameters.

    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, params=None):
        self.index = 0
        self.session = 0
        self.success = None
        self.timeout = 5

    def set_index(self, index):
        self.index = index

    def set_params(self, params):
        self.params = params

    def set_session(self, session):
        self.session = session

    def log(self, msg):
        self.session.log(msg)

    @abc.abstractproperty
    def run(self):
        """This method MUST be implemented by any derivated step to implement
        its own logic."""
        return

    def failed(self):
        if self.success == None:
            self.success = False

    def succeeded(self):
        if self.success == None:
            self.success = True

    def wait_status(self, timeout=None):
        """Wait during 'timeout' seconds that other thread completes the step.
        This can be used when the success or failure is determined in a callback
        function.
        """
        # Override default step timeout
        if timeout:
            self.timeout = timeout

        # Create a timer that will automatically trigger failure in this ste
        t = threading.Timer(self.timeout, self.failed)
        t.start()

        while self.success == None:
            time.sleep(0.5)

        if self.success == None:
            self.failed()
