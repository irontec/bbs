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

from clint.textui import colored

from step import Step


class LogStep(Step):

    def __init__(self):
        Step.__init__(self)
        self.message = None

    def set_params(self, params):
        self.message = params

    def run(self):
        if not self.message:
            self.failed()
        else:
            self.log(colored.yellow("-- [%s] %s" % (self.session.name, self.message)))
            self.succeeded()
