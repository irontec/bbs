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

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Settings(object):
    """
    This class will manage the unique instance of settings.

    Instance attributes:
      verbose: int
        Stores general verbosity level determined in command line
      keepon: bool = False
        If false, application will stop running scenarios after the first
        unsuccessful scenario.
      nameserver: str
        Stores nameservers determined in command line
      transport: str
        Force transport for all transactions
    """
    __metaclass__ = Singleton

    def __init__(self):
        self.verbose = 0
        self.nameserver = None
        self.keepon = False
        self.transport = None
