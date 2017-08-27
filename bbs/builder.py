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
        if name == "register":
            return register.RegisterStep()
        if name == "unregister":
            return unregister.UnregisterStep()
        if name == "waitfor":
            return waitfor.WaitforStep()
        if name == "wait":
            return wait.WaitStep()
        if name == "log":
            return log.LogStep()
        if name == "call":
            return call.CallStep()
        if name == "answer":
            return answer.AnswerStep()
        if name == "ringing":
            return ringing.RingingStep()
        if name == "dtmf":
            return dtmf.DtmfStep()
        if name == "hangup":
            return hangup.HangupStep()
        if name == "busy":
            return busy.BusyStep()
        if name == "callid":
            return callid.CallidStep()
        if name == "blindxfer":
            return blindxfer.BlindXferStep()
        if name == "attxfer":
            return attxfer.AttXferStep()

        raise Exception("Unknown step named " + name)
