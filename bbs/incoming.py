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


import re


def parse_name_addr_header(msg, names):
    """Find the first header with any of the given names in a SIP message
    and return a tuple (display name, uri) or None if not found.

    Display name may be quoted or not and may be followed or not by
    whitespace before the uri. Header names are case insensitive."""
    pattern = r'^(?:%s)[ \t]*:[ \t]*(?:"([^"]*)"|([^<\r\n]*?))[ \t]*<([^>]*)>' \
        % '|'.join(re.escape(name) for name in names)
    match = re.search(pattern, msg, re.MULTILINE | re.IGNORECASE)
    if not match:
        return None

    name = match.group(1) if match.group(1) is not None else match.group(2)
    name = name.strip() if name else None
    return (name or None, match.group(3))


def uri_host(uri):
    """Return the lowercase host (without port) of a sip/sips uri or None"""
    match = re.match(r'^sips?:(?:[^@;>]*@)?([^:;>?]+)', uri.strip(), re.IGNORECASE)
    if not match:
        return None
    return match.group(1).lower()


def uri_param_names(uri):
    """Return the lowercase names of the parameters of a sip/sips uri"""
    params = uri.strip().split('?', 1)[0].split(';')[1:]
    return [param.split('=', 1)[0].strip().lower() for param in params if param.strip()]


def parse_incoming_call(call, rdata):
    """Store caller information headers of an incoming INVITE in the call"""
    from pjsua import SIPUri

    msg = str(rdata.msg_info_buffer)

    call.pai_name = None
    call.pai = None
    call.pai_host = None
    call.from_uri = None
    call.from_host = None
    call.diversion = None
    call.contact_uri = None

    # Get callerid name and number from incoming call
    pai = parse_name_addr_header(msg, ["P-Asserted-Identity"])
    if pai:
        call.pai_name = pai[0]
        call.pai = SIPUri(pai[1])
        call.pai_host = uri_host(pai[1])

    # Get From uri from incoming call
    fromhdr = parse_name_addr_header(msg, ["From", "f"])
    if fromhdr:
        call.from_uri = SIPUri(fromhdr[1])
        call.from_host = uri_host(fromhdr[1])

    # Get Contact uri (without header params) from incoming call
    contact = parse_name_addr_header(msg, ["Contact", "m"])
    if contact:
        call.contact_uri = contact[1]

    # Get diversion.num from incoming call
    match = re.search("Diversion:[^\n]*<(.*)>[^\n]*\r\n", msg)
    if match:
        call.diversion = SIPUri(match.group(1))
