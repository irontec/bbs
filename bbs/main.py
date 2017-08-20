#!/usr/bin/env python
# encoding: utf-8
'''
bbs -- Black Box SIP Tester

Simple scenario tester for SIP using PJSIP-UA python bindings.

@author:     Ivan Alonso [a.k.a. Kaian] <kaian@irontec.com>

@copyright:  2017 Irontec S.L. All rights reserved.

@license:    GPL-3

@contact:    vozip@irontec.com
@deffield    updated: Updated
'''

__all__ = []
__version__ = 0.1
__date__ = '2017-03-31'
__updated__ = '2017-03-31'
__copyright__ = """
Copyright (C) 2017  Irontec S.L.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from argparse import ArgumentParser
import sys

from bbs.conf import ConfigParser
from bbs.junit.writer import JUnitWriter
from bbs.pjlib import PJLib
from bbs.scenario import Scenario
from bbs.settings import Settings


def main(argv=None):
    '''Command line options.'''

    program_version = "v%s" % __version__
    program_build_date = "%s" % __updated__

    program_longdesc = '''BBlack Box SIP Tester'''
    program_version_string = '%s %s (%s)' % (program_longdesc, program_version, program_build_date)
    program_license = '''License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>

    This is free software: you are free to change and redistribute it.

    There is NO WARRANTY, to the extent permitted by law.'''

    if argv is None:
        argv = sys.argv[1:]

    # setup option parser
    parser = ArgumentParser(description=program_longdesc, epilog=program_license)
    parser.add_argument("-V", "--version", action='version', version=program_version_string)
    parser.add_argument("-v", "--verbose", dest="verbose", default=0, action="count",
                      help="set verbosity level")
    parser.add_argument("-c", "--config", dest="config",
                      help="read configuration from file", metavar="FILE")
    parser.add_argument("-e", "--env", dest="env", metavar="FILE",
                      help="read environment data from file")
    parser.add_argument("-n", "--nameserver", dest="nameserver", nargs='+', metavar="NS",
                      help="Add the specified nameserver to enable SRV resolution")
    parser.add_argument("-o", "--output", dest="output", metavar="FILE",
                      help="output JUnit xml file")
    parser.add_argument("-k", "--keepon", dest="keepon", default=False, action="store_true",
                      help="do not stop on first failed scenario")

    # process options
    args = parser.parse_args(argv)

    if not args.config:
        parser.print_help()
        return 2
    try:
        config = ConfigParser.read_config(args.config, args.env)
    except Exception, e:
        print "Unable to parse config file %s: %s" % (args.config, e)
        return 2

    settings = Settings.instance()
    settings.verbose = args.verbose
    settings.nameserver = args.nameserver
    settings.keepon = args.keepon

    # Parse configuration scenarios
    scenarios = []
    for section in config:
        if section == "scenarios":
            for name in config[section]:
                scenarios.append(Scenario(name))

    # Initializa PJSUA
    lib = PJLib.instance()
    lib.init()

    # Run loaded scenarios
    for scenario in scenarios:
        scenario.run()
        if scenario.succeeded() is not True:
            if settings.keepon is False:
                break

    lib.deinit()

    # Save output if requested
    if args.output:
        junit = JUnitWriter()
        junit.save(args.output, scenarios)

    return 0
