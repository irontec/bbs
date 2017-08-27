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
from bbs.settings import Settings

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class PJLib(object):
    """
    This class will manage the unique instance of pjsip library.

    Instance attributes:
      lib: pjsua.Lib
        Unique PJSUA library instance used to create and destroy the SIP UA
        layer of PJSIP.
      transport: pjsua.Transport
        Default SIP UDP transport for all SIP messages.
    """
    __metaclass__ = Singleton

    def __init__(self):
        self.lib = None
        self.transport_udp = None
        self.transport_tcp = None
        self.transport_tls = None
        self.default_account_udp = None
        self.default_account_tcp = None
        self.default_account_tls = None

    def init(self):
        """Initialize global pjsip library.
        General codec and device configuration should be done here.
        """
        try:
            # Get log level from command line
            log_level = Settings().verbose
            nameserver = Settings().nameserver
            if nameserver:
                ua_cfg = pjsua.UAConfig()
                ua_cfg.nameserver = Settings().nameserver
            else:
                ua_cfg = None

            # Initializa PJSUA
            self.lib = pjsua.Lib()
            self.lib.init(log_cfg=pjsua.LogConfig(level=log_level, callback=self.pjlog_cb), ua_cfg=ua_cfg)
            self.transport_udp = self.lib.create_transport(pjsua.TransportType.UDP)
            self.transport_tcp = self.lib.create_transport(pjsua.TransportType.TCP)
            self.transport_tls = self.lib.create_transport(pjsua.TransportType.TLS)
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

    def get_default_account(self, transport=None):
        if transport == 'tcp':
            if not self.default_account_tcp:
                self.default_account_tcp = self.lib.create_account_for_transport(self.transport_tcp)
            return self.default_account_tcp
        elif transport == 'tls':
            if not self.default_account_tls:
                self.default_account_tls = self.lib.create_account_for_transport(self.transport_tls)
            return self.default_account_tls
        else:
            if not self.default_account_udp:
                self.default_account_udp = self.lib.create_account_for_transport(self.transport_udp)
            return self.default_account_udp
