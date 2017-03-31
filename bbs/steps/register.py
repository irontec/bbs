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

from pjsua import Lib, AccountConfig, AccountCallback

from credentials import CredentialsStep


class RegisterStep(CredentialsStep, AccountCallback):

    def __init__(self):
        CredentialsStep.__init__(self)

    def on_reg_state(self):
        # Set session account
        self.session.account = self.account
        # Check if register has succeeded
        self.success = self.account.info().reg_status == 200

    def on_incoming_call(self, call):
        manager = self.session.get_manager()
        call.set_callback(manager)
        manager.on_state()

    def run(self):
        self.log("-- [%s] Running %s " % (self.session.name, self.__class__.__name__))
        acc_cfg = AccountConfig(self.domain, self.username, self.password)
        self.session.account = Lib.instance().create_account(acc_cfg, False, self)
        self.wait_status()



