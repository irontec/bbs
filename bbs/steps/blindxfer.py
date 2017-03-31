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

from step import Step


class BlindXferStep(Step):

    def __init__(self, call=None):
        Step.__init__(self)
        self.number = None
        self.call = None

    def set_params(self, params):

        if type(params) is str:
            self.number = params

        if type(params) is int:
            self.number = str(params)

        if type(params) is dict:
            self.number = str(params['number'])
            if 'call' in params:
                self.call = params['call']

        if type(params) is list:
            self.call = params.pop(0)
            self.number = params.pop(0)

    def run(self):
        self.log("-- [%s] Running %s to number %s" % (self.session.name, self.__class__.__name__, self.number))
        reg_uri = SIPUri(self.session.account.info().uri)

        # Build the called URI
        desturi = "%s:%s@%s" % (reg_uri.scheme, self.number, reg_uri.host)

        # Get a new manager to handle events on this new call
        call = self.session.get_call(self.call)
        if call:
            # Make the call
            call.transfer(desturi, self.session)
            self.succeeded()
        else:
            self.failed()

