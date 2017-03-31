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

from step import Step


class UnregisterStep(Step):

    def __init__(self):
        Step.__init__(self)

    def run(self):
        self.log("-- [%s] Running %s " % (self.session.name, self.__class__.__name__))
        if self.session.account:
            self.session.account.delete()
            self.session.account = None
            self.succeeded()
        else:
            self.failed()



