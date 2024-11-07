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
from pjsua import Lib, AccountConfig, AccountCallback, SIPUri
from bbs.steps.step import Step
from bbs.settings import Settings


class RegisterStep(Step, AccountCallback):

    def __init__(self):
        self.username = None
        self.password = None
        self.domain = None
        self.transport = None
        Step.__init__(self)
        AccountCallback.__init__(self)

    def set_params(self, params):
        forced_transport = Settings().transport
        if forced_transport:
            self.transport = forced_transport

        if isinstance(params, dict):
            self.username = str(params['username'])
            self.password = str(params['password'])
            self.domain = str(params['domain'])
            if 'transport' in params and not forced_transport:
                self.transport = str(params['transport']).lower()

        if isinstance(params, list):
            self.username = str(params.pop(0))
            self.password = str(params.pop(0))
            self.domain = str(params.pop(0))
            if params and not forced_transport:
                self.transport = str(params.pop(0))

    def on_reg_state(self):
        # Set session account
        self.session.account = self.account
        # Check if register has succeeded
        self.success = self.account.info().reg_status == 200

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
        self.log("-- [%s] Running %s " % (self.session.name, self.__class__.__name__))
        if self.transport:
            self.domain += ';transport={}'.format(self.transport)
        acc_cfg = AccountConfig(self.domain, self.username, self.password)
        if Settings().exclusive:
            acc_cfg.transport_id = Lib.instance().create_transport(pjsua.TransportType.UDP)._id
        self.session.account = Lib.instance().create_account(acc_cfg, False, self)
        self.wait_status()
