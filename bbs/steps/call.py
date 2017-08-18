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

from pjsua import SIPUri
from bbs.pjlib import PJLib
from bbs.steps.step import Step


class CallStep(Step):

    def __init__(self, call=None):
        Step.__init__(self)
        self.number = None
        self.name = None
        self.uri = None
        self.callidnum = None
        self.hdrs = []

    def set_params(self, params):

        if isinstance(params, str):
            if '@' in params:
                self.uri = params
            else:
                self.number = params

        if isinstance(params, int):
            self.number = str(params)

        if isinstance(params, dict):
            if 'number' in params:
                self.number = str(params['number'])
            if 'uri' in params:
                self.uri = str(params['uri'])
            if 'callidnum' in params:
                self.callidnum = str(params['callidnum'])
            if 'name' in params:
                self.name = params['name']

        if isinstance(params, list):
            self.name = params.pop(0)
            self.number = params.pop(0)

    def run(self):
        try:
            # If not account is set, use default one
            if not self.session.account:
                self.session.account = PJLib.instance().get_default_account()

            if self.uri:
                self.log("-- [%s] Running %s to uri %s"
                         % (self.session.name, self.__class__.__name__, self.uri))
                desturi = self.uri
            else:
                self.log("-- [%s] Running %s to number %s"
                         % (self.session.name, self.__class__.__name__, self.number))
                reg_uri = SIPUri(self.session.account.info().uri)
                desturi = "%s:%s@%s" % (reg_uri.scheme, self.number, reg_uri.host)

            # Get a new manager to handle events on this call
            manager = self.session.get_manager(self.name)

            if self.callidnum:
                reg_uri = SIPUri(self.session.account.info().uri)
                pai_hdr = ("P-Asserted-Identity", "<%s:%s@%s>"
                           % (reg_uri.scheme, self.callidnum, reg_uri.host))
                self.hdrs.append(pai_hdr)

            self.session.account.make_call(desturi, manager, self.hdrs)
            self.succeeded()
        except:
            self.failed()
