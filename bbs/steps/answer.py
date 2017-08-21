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

"""Black Box SIP Answer session Step

This modules handles the BBS session step 'answer' in charge of answering
incoming calls.

"""
from bbs.steps.step import Step

class AnswerStep(Step):
    """
    This class will manage the steps named as 'answer' in any session.

    This step is designed to be used after manager has received the event
    INCOMING. If there are multiple incoming calls, the name parameter can be
    used to determine which one will be answered.
    """
    def __init__(self):
        Step.__init__(self)
        self.name = None

    def set_params(self, params):
        if isinstance(params, str):
            self.name = params
        if isinstance(params, dict):
            self.name = params['name']

    def run(self):
        self.log("-- [%s] Running %s " % (self.session.name, self.__class__.__name__))
        call = self.session.get_call(self.name)
        if call:
            call.answer()
            self.succeeded()
        else:
            self.failed()
