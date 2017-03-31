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

import pjsua

from step import Step


class DtmfStep(Step):

    def __init__(self):
        Step.__init__(self)
        self.call = None
        self.digit = None

    def set_params(self, params):

        if type(params) is str:
            self.digit = params
        if type(params) is int:
            self.digit = str(params)
        if type(params) is list:
            self.call = params.pop(0)
            self.digit = str(params.pop(0))
        if type(params) is dict:
            self.name = str(params['call'])
            self.digit = str(params['digit'])

    def run(self):
        self.log("-- [%s] Running %s with DTMF digit %s " % (self.session.name, self.__class__.__name__, self.digit))

        if not self.digit:
            self.failed()

        call = self.session.get_call(self.call)
        if call == None:
            self.failed()
        elif call.is_valid() == 0:
            self.failed()
        elif call.info().media_state != pjsua.MediaState.ACTIVE:
            self.failed()
        else:
            call.dial_dtmf(self.digit)
            self.succeeded()
