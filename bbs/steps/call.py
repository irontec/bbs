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
from ..pjlib import PJLib
from step import Step


class CallStep(Step):

    def __init__(self, call=None):
        Step.__init__(self)
        self.number = None
        self.name = None
        self.uri = None

    def set_params(self, params):

        if type(params) is str:
            if '@' in params:
                self.uri = params
            else:
                self.number = params

        if type(params) is int:
            self.number = str(params)

        if type(params) is dict:
            self.number = str(params['number'])
            if 'name' in params:
                self.name = params['name']

        if type(params) is list:
            self.name = params.pop(0)
            self.number = params.pop(0)

    def run(self):
        try:
            if self.uri:
                self.log("-- [%s] Running %s to uri %s" % (self.session.name, self.__class__.__name__, self.uri))
                desturi=self.uri
            else:
                self.log("-- [%s] Running %s to number %s" % (self.session.name, self.__class__.__name__, self.number))
                reg_uri = SIPUri(self.session.account.info().uri)
                desturi = "%s:%s@%s" % (reg_uri.scheme, self.number, reg_uri.host)

            # Get a new manager to handle events on this call
            manager = self.session.get_manager(self.name)

            # Make the call
            if not self.session.account:
                self.session.account = PJLib.instance().get_default_account()
            self.session.account.make_call(desturi, manager)
            self.succeeded()
        except:
            self.failed()

