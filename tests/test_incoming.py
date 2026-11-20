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


import unittest

from bbs.incoming import parse_name_addr_header, uri_host


def message(*headers):
    lines = ["INVITE sip:999333002@10.177.103.35 SIP/2.0"] + list(headers) + ["Content-Length: 0", "", ""]
    return "\r\n".join(lines)


class ParseNameAddrHeaderTest(unittest.TestCase):

    def test_pai_without_display_name(self):
        msg = message("P-Asserted-Identity: <sip:999444000@example.com>")
        self.assertEqual(parse_name_addr_header(msg, ["P-Asserted-Identity"]),
                         (None, "sip:999444000@example.com"))

    def test_pai_with_quoted_display_name_and_space(self):
        msg = message("P-Asserted-Identity: \"BBS Caller\" <sip:999444000@example.com>")
        self.assertEqual(parse_name_addr_header(msg, ["P-Asserted-Identity"]),
                         ("BBS Caller", "sip:999444000@example.com"))

    def test_pai_with_quoted_display_name_without_space(self):
        msg = message("P-Asserted-Identity: \"BBS Caller\"<sip:999444000@example.com>")
        self.assertEqual(parse_name_addr_header(msg, ["P-Asserted-Identity"]),
                         ("BBS Caller", "sip:999444000@example.com"))

    def test_pai_with_unquoted_display_name(self):
        msg = message("P-Asserted-Identity: BBS<sip:999444000@example.com>")
        self.assertEqual(parse_name_addr_header(msg, ["P-Asserted-Identity"]),
                         ("BBS", "sip:999444000@example.com"))

    def test_header_name_is_case_insensitive(self):
        msg = message("p-asserted-identity: <sip:999444000@example.com;user=phone>")
        self.assertEqual(parse_name_addr_header(msg, ["P-Asserted-Identity"]),
                         (None, "sip:999444000@example.com;user=phone"))

    def test_missing_header(self):
        msg = message("From: <sip:alice@example.com>;tag=1")
        self.assertIsNone(parse_name_addr_header(msg, ["P-Asserted-Identity"]))

    def test_from_header_ignores_tag(self):
        msg = message("From: \"Alice\" <sip:alice@example.com>;tag=1234")
        self.assertEqual(parse_name_addr_header(msg, ["From", "f"]),
                         ("Alice", "sip:alice@example.com"))

    def test_compact_from_header(self):
        msg = message("f: <sip:alice@example.com>;tag=1234")
        self.assertEqual(parse_name_addr_header(msg, ["From", "f"]),
                         (None, "sip:alice@example.com"))

    def test_from_does_not_match_other_headers_ending_in_from(self):
        msg = message("X-Forwarded-From: <sip:other@example.com>", "From: <sip:alice@example.com>;tag=1")
        self.assertEqual(parse_name_addr_header(msg, ["From", "f"]),
                         (None, "sip:alice@example.com"))


class UriHostTest(unittest.TestCase):

    def test_host_without_port(self):
        self.assertEqual(uri_host("sip:999444000@example.com"), "example.com")

    def test_host_with_port_and_params(self):
        self.assertEqual(uri_host("sip:999444000@Example.COM:5060;user=phone"), "example.com")

    def test_uri_without_user(self):
        self.assertEqual(uri_host("sips:example.com;transport=tls"), "example.com")

    def test_ipv4_host(self):
        self.assertEqual(uri_host("sip:alice@10.177.103.35:4060"), "10.177.103.35")

    def test_tel_uri_has_no_host(self):
        self.assertIsNone(uri_host("tel:+34600111222"))


if __name__ == '__main__':
    unittest.main()
