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

import pjsua

from settings import Settings


class PJLib(object):
    """
    This class will manage the unique instance of pjsip library.
    Rest of the process can access this library by using the static
    class method instance()

    Class attributes:
      _instance: PJLib
        Stores the only instance of this class that must be accessed using the
        class method instance().

    Instance attributes:
      lib: pjsua.Lib
        Unique PJSUA library instance used to create and destroy the SIP UA
        layer of PJSIP.
      transport: pjsua.Transport
        Default SIP UDP transport for all SIP messages.
    """
    _instance = None

    def __init__(self):
        self.lib = None
        self.transport = None

    @staticmethod
    def instance():
        """Static class method to retrieve the unique instance of PJLib"""
        if not PJLib._instance:
            PJLib._instance = PJLib()
        return PJLib._instance


    def init(self):
        """Initialize global pjsip library.
        General codec and device configuration should be done here.
        """
        try:
            # Get log level from command line
            log_level = Settings.instance().verbose
            nameserver = Settings.instance().nameserver
            if nameserver:
                ua_cfg = pjsua.UAConfig()
                ua_cfg.nameserver = Settings.instance().nameserver
            else:
                ua_cfg = None

            # Initializa PJSUA
            self.lib = pjsua.Lib()
            self.lib.init(log_cfg=pjsua.LogConfig(level=log_level, callback=self.pjlog_cb), ua_cfg=ua_cfg)
            self.transport = self.lib.create_transport(pjsua.TransportType.UDP)
            self.default_account = self.lib.create_account_for_transport(self.transport)
            self.lib.set_null_snd_dev()
            self.lib.start()
        except pjsua.Error, e:
            self.lib.destroy()
            print "Exception: " + str(e)


    def deinit(self):
        """Deinitialization of global pjsil library.
        This ensure that all accounts are properly unregistered and calls are
        hanguped up gracefully before leaving"""
        if self.lib:
            self.lib.hangup_all()
            self.lib.destroy()

    def pjlog_cb(self, level, str, len):
        """Generic Log callbac for PJSUA library"""
        print str,

    def get_default_account(self):
        return self.default_account
