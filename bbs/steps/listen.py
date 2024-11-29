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

import re
import pjsua
from clint.textui import colored
from pjsua import Lib, AccountConfig, AccountCallback, SIPUri
from bbs.pjlib import PJLib
from bbs.steps.step import Step
from bbs.settings import Settings


class ListenStep(Step, AccountCallback):

    def __init__(self):
        self.address = "0.0.0.0"
        self.port = 5060
        self.externip = None
        self.transport = pjsua.TransportType.UDP
        Step.__init__(self)
        AccountCallback.__init__(self)

    def set_params(self, params):
        forced_transport = Settings().transport
        if forced_transport:
            self.transport = PJLib().transport_str_to_pjsua(forced_transport)

        if isinstance(params, dict):
            self.address = str(params['address'])
            self.port = params['port']
            self.externip = params['externip']
            if 'transport' in params and not forced_transport:
                self.transport = PJLib().transport_str_to_pjsua(str(params['transport']).lower())

        if isinstance(params, list):
            self.port = params.pop(0)
            if params:
                self.address = str(params.pop(0))
            if params:
                self.externip = str(params.pop(0))
            if params and not forced_transport:
                self.transport = PJLib().transport_str_to_pjsua(str(params.pop(0)))

    def on_incoming_call2(self, call, rdata):
        # Let the manager handle this call events
        manager = self.session.get_manager()
        call.set_callback(manager)
        call.pai_name = None
        call.pai = None
        call.diversion = None
        # Get callerid name and number from incoming call
        match = re.search("P-Asserted-Identity: (?:\"([^\"]+)\" )?<(.*)>\r\n", str(rdata.msg_info_buffer))
        if match:
            call.pai_name = match.group(1)
            call.pai = SIPUri(match.group(2))
        # Get diversion.num from incoming call
        match = re.search("Diversion:[^\n]*<(.*)>[^\n]*\r\n", str(rdata.msg_info_buffer))
        if match:
            call.diversion = SIPUri(match.group(1))
        # Notify incoming event state
        manager.on_state()

    def run(self):
        self.log("-- [%s] Running %s for transport %s:%d [%s]" % (self.session.name, self.__class__.__name__, self.address, self.port, self.externip))
        transport =  PJLib().lib.create_transport(pjsua.TransportType.UDP, pjsua.TransportConfig(self.port, self.address, self.externip))
        self.session.account =  PJLib().lib.create_account_for_transport(transport, True, self)
        self.succeeded()
