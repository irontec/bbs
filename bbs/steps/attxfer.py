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

class AttXferStep(Step):

    def __init__(self, call=None):
        Step.__init__(self)
        self.call = None
        self.target = None

    def set_params(self, params):

        if type(params) is str:
            self.target = params

        if type(params) is dict:
            self.target = params['target']
            if 'call' in params:
                self.call = params['call']

        if type(params) is list:
            self.call = params.pop(0)
            self.target = params.pop(0)

    def run(self):
        self.log("-- [%s] Running %s to target %s" % (self.session.name, self.__class__.__name__, self.target))

        # Get a new manager to handle events on this new call
        call = self.session.get_call(self.call)
        target = self.session.get_call(self.target)
        if call and target:
            # Make the call
            call.transfer_to_call(target, self.session)
            self.succeeded()
        else:
            self.failed()
