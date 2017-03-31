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

from step import Step

from ..pjlib import PJLib


class CredentialsStep(Step, AccountCallback):

    def __init__(self):
        Step.__init__(self)
        AccountCallback.__init__(self, None)

    def set_params(self, params):

        if type(params) is dict:
            self.username = params['username']
            self.password = params['password']
            self.domain = params['domain']

        if type(params) is list:
            self.username = params.pop(0)
            self.password = params.pop(0)
            self.domain = params.pop(0)

    def run(self):
        self.log("-- [%s] Running %s " % (self.session.name, self.__class__.__name__))
        # Setup account with given credentials, but without register URI
        acc_cfg = AccountConfig(self.domain, self.username, self.password)
        acc_cfg.reg_uri = None
        # Set default transport for this accounts
        acc_cfg.transport_id = PJLib.instance().transport._id
        # Create the account and associate to the session
        self.session.account = Lib.instance().create_account(acc_cfg, False, self)
        # We don't register, so there's no way to check if credentials are
        # correct at this point
        self.succeeded()



