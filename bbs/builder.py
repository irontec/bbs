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

from bbs.steps import *


class StepBuilder(object):

    @staticmethod
    def from_name(name):

        steps = {
            'register': register.RegisterStep(),
            'unregister': unregister.UnregisterStep(),
            'waitfor': waitfor.WaitforStep(),
            'wait': wait.WaitStep(),
            'log': log.LogStep,
            'call': call.CallStep(),
            'answer': answer.AnswerStep(),
            'ringing': ringing.RingingStep(),
            'dtmf': dtmf.DtmfStep(),
            'hangup': hangup.HangupStep(),
            'busy': busy.BusyStep(),
            'redirect': redirect.RedirectStep(),
            'hold': hold.HoldStep(),
            'unhold': unhold.UnholdStep(),
            'callid': callid.CallidStep(),
            'callidname': callidname.CallidNameStep(),
            'diversion': diversion.DiversionStep(),
            'blindxfer': blindxfer.BlindXferStep(),
            'attxfer': attxfer.AttXferStep(),
            'listen': listen.ListenStep(),
        }

        if name.lower() in steps:
            return steps[name.lower()]

        raise Exception("Unknown step named " + name)
