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

from optparse import OptionParser
import sys, os

from conf import ConfigParser
from junit.writer import JUnitWriter
from pjlib import PJLib
from scenario import Scenario
from settings import Settings


def main(argv=None):
    '''Command line options.'''

    program_version = "v%s" % __version__
    program_build_date = "%s" % __updated__

    program_version_string = '%%prog %s (%s)' % (program_version, program_build_date)
    program_longdesc = '''BBlack Box SIP Tester'''
    program_license = '''License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>

    This is free software: you are free to change and redistribute it.

    There is NO WARRANTY, to the extent permitted by law.'''

    if argv is None:
        argv = sys.argv[1:]

    # setup option parser
    parser = OptionParser(version=program_version_string, epilog=program_longdesc, description=program_license)
    parser.add_option("-v", "--verbose", dest="verbose", default=0, action="count",
                      help="set verbosity level [default: %default]")
    parser.add_option("-c", "--config", dest="config",
                      help="read configuration from file", metavar="FILE")
    parser.add_option("-e", "--env", dest="env",
                      help="read environment data from file", metavar="FILE")
    parser.add_option("-o", "--output", dest="output",
                      help="output JUnit xml file", metavar="FILE")
    parser.add_option("-k", "--keepon", dest="keepon", default=False, action="store_true",
                      help="do not stop on first failed scenario")

    # process options
    (opts, args) = parser.parse_args(argv)

    if not opts.config:
        parser.print_help()
        return 2
    try:
        config = ConfigParser.read_config(opts.config, opts.env)
    except Exception, e:
        print "Unable to parse config file %s: %s" % (opts.config, e)
        return 2

    settings = Settings.instance()
    settings.verbose = opts.verbose
    settings.keepon = opts.keepon

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
    if opts.output:
        junit = JUnitWriter()
        junit.save(opts.output, scenarios)

    return 0

