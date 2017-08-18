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


class WaitforStep(Step):

    def __init__(self):
        Step.__init__(self)
        self.event = None

    def set_params(self, params):

        if type(params) is dict:
            self.event = params

        if type(params) is str:
            self.event = { "name": params }

    def run(self):
        self.log("-- [%s] Running %s on event %s" % (self.session.name, self.__class__.__name__, self.event['name']))

        while self.success == None:

            if not self.session.events:
                continue

            event = self.session.events.pop(0)

            if 'call' in self.event.keys():
                if self.event['call'] != event['call']:
                    continue

            if 'name' in self.event.keys():
                if self.event['name'].lower() != event['name'].lower():
                    continue

            self.succeeded()

#             if self.event['code'] != None and self.event['code'] == event['code']:
#                 self.succeeded()
#                 continue
#
#             if self.event['reason'] != None and self.event['reason'] == event['reason']:
#                 self.succeeded()
#                 continue
