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

from junit_xml import TestCase, TestSuite


class JUnitWriter(object):

    def save(self, filename, scenarios):
        suite = TestSuite(filename)

        for scenario in scenarios:
            case = TestCase(scenario.name)
            suite.test_cases.append(case)
            if not scenario.succeeded():
                case.add_error_info("\n".join(scenario.messages))

        # pretty printing is on by default but can be disabled using prettyprint=False
        with open(filename, 'w') as f:
            TestSuite.to_file(f, [ suite ], prettyprint=False)
