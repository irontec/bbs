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

from time import sleep
from bbs.steps.step import Step


class RingingStep(Step):

    def __init__(self):
        Step.__init__(self)
        self.name = None
        self.time = 0

    def set_params(self, params):
        if isinstance(params, str):
            self.name = params
        if isinstance(params, int):
            self.time = params
        if isinstance(params, dict):
            self.name = params['name']
            self.time = int(params['time'])

    def run(self):
        self.log("-- [%s] Running %s [%d seconds]" % (self.session.name, self.__class__.__name__, self.time))
        call = self.session.get_call(self.name)
        if call:
            call.answer(180)
            if self.time:
                sleep(self.time)
            self.succeeded()
        else:
            self.failed()
