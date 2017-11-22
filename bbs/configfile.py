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

import yaml


class ConfigFile(object):
    """Parse configuration files into python structures containing scenarios
    """

    def __init__(self, filename):
        self.filename = filename
        self.scenarios = []

    def __str__(self):
        return self.filename

    def add_scenario(self, scenario):
        self.scenarios.append(scenario)

    def parse(self, env_file=None):
        yaml_stream = ""

        # Open environment file if any
        if env_file:
            try:
                yaml_stream += open(env_file, 'r').read()
            except (OSError, IOError) as ex:
                print "Error opening %s: %s" % (env_file, ex)

        # Open configuration file
        try:
            yaml_stream += open(self.filename, 'r').read()
        except (OSError, IOError) as ex:
            print "Error opening %s: %s" % (self.filename, ex)

        # Try to parse concatenated configuration files
        try:
            return yaml.load(yaml_stream)
        except yaml.YAMLError as ex:
            print "Error parsing configuration yaml: ", ex