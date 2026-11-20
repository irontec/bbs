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

class NoPaiStep(Step):

    def run(self):
        self.log("-- [%s] Checking there is no P-Asserted-Identity " % self.session.name)
        call = self.session.get_call()
        if call and getattr(call, 'pai', None) is None:
            self.succeeded()
            return

        self.failed()
