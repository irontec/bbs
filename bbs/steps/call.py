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
        self.dest = None
        self.name = None
        self.callidnum = None
        self.diversion = []
        self.hdrs = []

    def set_params(self, params):

        if isinstance(params, str):
            self.dest = params

        if isinstance(params, int):
            self.dest = str(params)

        if isinstance(params, dict):
            if 'name' in params:
                self.name = params['name']
            if 'dest' in params:
                self.dest = str(params['dest'])
            if 'callidnum' in params:
                self.callidnum = str(params['callidnum'])
            if 'diversion' in params:
                self.diversion = params['diversion']

        if isinstance(params, list):
            self.name = params.pop(0)
            self.dest = params.pop(0)
            self.callidnum = params.pop(0)

    def create_uri(self, candidate='12345'):
        """Given a number, create uri with registry uri.
        Given an uri, return that uri"""

        if ':' in candidate:
            final_uri = candidate
        else:
            reg_uri = SIPUri(self.session.account.info().uri)
            final_uri = "%s:%s@%s" % (reg_uri.scheme, candidate, reg_uri.host)

        return final_uri

    def add_header(self, hdr_name, hdr_uri):
        """Add SIP header with a given URI"""
        uri = self.create_uri(hdr_uri)
        hdr = (hdr_name, "<{}>".format(uri))
        self.log("-- [{}] Adding {} header: '{}'".format(self.session.name, hdr[0], hdr[1]))
        self.hdrs.append(hdr)

    def run(self):
        try:
            # If not account is set, use default one
            if not self.session.account:
                self.session.account = PJLib().get_default_account()

            # Dest-URI
            desturi = self.create_uri(self.dest)
            self.log("-- [%s] Calling %s to uri %s"
                     % (self.session.name, self.__class__.__name__, desturi))

            # P-Asserted-Identity
            if self.callidnum:
                self.add_header("P-Asserted-Identity", self.callidnum)

            # Diversion header(s)
            for div in self.diversion:
                self.add_header("Diversion", div)

            # Get a new manager to handle events on this call
            manager = self.session.get_manager(self.name)

            self.session.account.make_call(desturi, manager, self.hdrs)
            self.succeeded()
        except:
            self.failed()
