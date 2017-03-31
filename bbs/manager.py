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

from pjsua import Lib, CallCallback, MediaState


class CallManager(CallCallback):

    def __init__(self, name, session):
        self.name = name
        self.session = session

    def on_media_state(self):
        if self.call.info().media_state == MediaState.ACTIVE:
            call_slot = self.call.info().conf_slot
            Lib.instance().conf_connect(call_slot, 0)
            Lib.instance().conf_connect(0, call_slot)

    # Notification when call state has changed
    def on_state(self):
        """ Keep track of all of this call state changes """
        event = {}
        event['call'] = self.name
        event['name'] = self.call.info().state_text
        event['code'] = self.call.info().last_code
        event['reason'] = self.call.info().last_reason
        self.session.add_event(event)

    # Notifications when transfer state has changed
    def on_transfer_status(self, code, reason, final, cont):
        """ Keep track of all of this call state changes """
        event = {}
        event['call'] = self.name
        event['name'] = ("TRANSFER_%s" % reason)
        event['code'] = code
        event['reason'] = reason
        self.session.add_event(event)
