#!/usr/bin/env python
# encoding: utf-8
"""
bbs -- Black Box SIP Tester

Simple scenario tester for SIP using PJSIP-UA python bindings.

@author:     Ivan Alonso [a.k.a. Kaian] <kaian@irontec.com>

@copyright:  2017 Irontec S.L. All rights reserved.

@license:    GPL-3

@contact:    vozip@irontec.com
@deffield    updated: Updated
"""

__all__ = []
__progname__ = 'bbs'
__version__ = 0.1
__date__ = '2017-03-31'
__updated__ = '2017-08-21'
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

import sys
from argparse import ArgumentParser
from bbs.junit.writer import JUnitWriter
from bbs.pjlib import PJLib
from bbs.scenario import Scenario
from bbs.settings import Settings
from bbs.configfile import ConfigFile


def main(argv=None):
    """Entry point of the program

    This function will handle command line arguments and create required
    instances in order to run the configuration scenarios.

    Args:
        argv (list, optional): List of command line flags and arguments.

    Returns:
        0 in case of success
        1 in case of command line parsing errors
        2 in case of configuration files parsing errors
    """

    program_longdesc = "Black Box SIP Tester"
    program_version = '%s v%s (%s)' % (__progname__, __version__, __updated__)
    program_license = """
    License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
    This is free software: you are free to change and redistribute it.
    There is NO WARRANTY, to the extent permitted by law.
    """
    program_longdesc = "Simple scenario tester for SIP using PJSIP-UA python bindings."

    if argv is None:
        argv = sys.argv[1:]

    # setup option parser
    parser = ArgumentParser(description=program_longdesc, epilog=program_license)
    parser.add_argument("-V", "--version", action='version', version=program_version)
    parser.add_argument("-v", "--verbose", dest="verbose", default=0, action="count",
                        help="set verbosity level")
    parser.add_argument("-c", "--config", dest="config", nargs='+',
                        help="read configuration from file", metavar="FILE")
    parser.add_argument("-e", "--env", dest="env", metavar="FILE",
                        help="read environment data from file")
    parser.add_argument("-n", "--nameserver", dest="nameserver", nargs='+', metavar="NS",
                        help="Add the specified nameserver to enable SRV resolution")
    parser.add_argument("-o", "--output", dest="output", metavar="FILE",
                        help="output JUnit xml file")
    parser.add_argument("-k", "--keepon", dest="keepon", default=False, action="store_true",
                        help="do not stop on first failed scenario")
    parser.add_argument("-t", "--transport", choices=['udp', 'tcp', 'tls'], dest="transport",
                        help="Force UDP/TCP/TLS for all transactions")
    parser.add_argument("-x", "--exclusive", dest="exclusive", default=False, action="store_true",
                        help="Create a new transport for each agent")
    parser.add_argument("-s", "--stdcodecs", dest="stdcodecs", default=False, action="store_true",
                        help="Only use PCMA and PCMU codecs")

    # process options
    args = parser.parse_args(argv)

    if not args.config:
        parser.print_help()
        return 1

    # Set global settings
    settings = Settings()
    settings.verbose = args.verbose
    settings.nameserver = args.nameserver
    settings.keepon = args.keepon
    settings.transport = args.transport
    settings.exclusive = args.exclusive
    settings.stdcodecs = args.stdcodecs

    # read environment configuration
    config_files = []
    for file in args.config:
        conf_file = ConfigFile(file)
        configuration = conf_file.parse(args.env)

        if not configuration:
            return 2

        for section in configuration:
            if section == "scenarios":
                for scenario_params in configuration[section]:
                    scenario = Scenario(conf_file, scenario_params)
                    conf_file.add_scenario(scenario)

        config_files.append(conf_file)

    if not config_files:
        print "No valid configuration files found, quitting..."
        return 2

    # Initializa PJSUA
    lib = PJLib()
    lib.init()


    # Default exit code if all test succeded
    exitcode = 0

    # Run loaded scenarios
    for config_file in config_files:
        for scenario in config_file.scenarios:
            scenario.run()
            if scenario.succeeded() is not True:
                exitcode = 1
                if settings.keepon is False:
                    break

    lib.deinit()

    # Save output if requested
    if args.output:
        junit = JUnitWriter()
        junit.save(args.output, config_files)

    return exitcode


if __name__ == "__main__":
    main()
