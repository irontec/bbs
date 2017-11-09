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

from bbs.steps.step import Step
from pjsua import SIPUri


class RedirectStep(Step):

    def __init__(self):
        Step.__init__(self)
        self.name = None
        self.dest = None
        self.reason = 'deflection'

    def set_params(self, params):
        if isinstance(params, int):
            self.dest = str(params)
        if isinstance(params, str):
            self.dest = params
        if isinstance(params, dict):
            self.dest = str(params['dest'])
            if 'name' in params:
                self.name = params['name']
            if 'reason' in params:
                self.reason = params['reason']

    def create_contact(self, candidate, reason):
        """Given a number, create Contact header with registry uri.
        Given an uri, return that uri in Contact header"""
        if ':' in candidate:
            final_contact = "<%s>;reason=%s" % (candidate, reason)
        else:
            reg_uri = SIPUri(self.session.account.info().uri)
            final_contact = "<%s:%s@%s>;reason=%s" % (reg_uri.scheme, candidate, reg_uri.host, reason)

        return final_contact

    def run(self):
        self.log("-- [%s] Running %s " % (self.session.name, self.__class__.__name__))
        call = self.session.get_call(self.name)
        if call:
            contact_hdr = self.create_contact(self.dest, self.reason)
            call.hangup(code=302, reason="Moved Temporarily", hdr_list=[('Contact', contact_hdr)])
            self.succeeded()
        else:
            self.failed()
