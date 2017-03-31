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

import time

from step import Step


class WaitStep(Step):

    def __init__(self):
        Step.__init__(self)
        self.stime = 1

    def set_params(self, params):
        if not params:
            return

        if type(params) is int:
            self.stime = params

        if type(params) is dict:
            if 'time' in params.keys():
                self.stime = params['time']

    def run(self):
        self.log("-- [%s] Running %s [%s seconds] " % (self.session.name, self.__class__.__name__, self.stime))

        time.sleep(self.stime)
        self.succeeded()
