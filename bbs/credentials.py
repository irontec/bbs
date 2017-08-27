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

class Credentials(AccountCallback):
    def __init__(self, params):
        if isinstance(params, dict):
            self.username = str(params['username'])
            self.password = str(params['password'])
            self.domain = str(params['domain'])

        if isinstance(params, list):
            self.username = str(params.pop(0))
            self.password = str(params.pop(0))
            self.domain = str(params.pop(0))
        AccountCallback.__init__(self, None)

    def get_account(self):
        acc_cfg = AccountConfig(self.domain, self.username, self.password)
        acc_cfg.reg_uri = None
        return Lib.instance().create_account(acc_cfg, False, self)
