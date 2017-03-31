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

class Settings(object):
    """
    This class will manage the unique instance of settings.
    Rest of the process can access application settings by using the static
    class method instance()

    Class attributes:
      _instance: PJLib
        Stores the only instance of this class that must be accessed using the
        class method instance().

    Instance attributes:
      verbose: int
        Stores general verbosity level determined in command line
      keepon: bool = False
        If false, application will stop running scenarios after the first
        unsuccessful scenario.
    """
    _instance = None

    def __init__(self):
        self.verbose = 0
        self.keepon = False

    @staticmethod
    def instance():
        """Static class method to retrieve the unique instance of Settings"""
        if not Settings._instance:
            Settings._instance = Settings()
        return Settings._instance

