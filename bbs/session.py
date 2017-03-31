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

from threading import Thread

from clint.textui import colored
from pjsua import Lib

from manager import CallManager


class Session(object):

    account = None

    def __init__(self, name, scenario):
        self.name = name
        self.scenario = scenario
        self.steps = []
        self.events = []
        self.messages = []
        self.account = None
        self.calls = {}
        self.thread = None

    def __repr__(self, *args, **kwargs):
        return 'Session(' + repr(self.name) + ', ' + repr(self.steps) + ')';

    def add_step(self, step):
        step.set_session(self)
        self.steps.append(step)

    def get_manager(self, name=None):
        if name not in self.calls:
            self.calls[name] = CallManager(name, self)
        return self.calls[name]

    def get_call(self, name=None):
        if name in self.calls:
            return self.calls[name].call

        if len(self.calls.keys()) == 1:
            return next(iter(self.calls.values())).call

        return None

    def log(self, msg):
        self.messages.append(msg)
        self.scenario.log(msg)

    def add_event(self, event):
        if not 'code' in event.keys():
            event['code'] = 0

        if not 'reason' in event.keys():
            event['reason'] = ""

        if not 'call' in event.keys():
            event['call'] = None

        event_text = "%s [%s]" % (event['name'], event['code'])
        if event['call']:
            event_text += " on %s" % (event['call'])

        self.log(colored.magenta("  >> [%s] Received event %s" % (self.name, event_text)))
        self.events.append(event)

    def completed(self):
        steps_ok = 0
        for step in self.steps:
            if step.success == None:
                continue
            if step.success == True:
                steps_ok += 1
            else:
                print step.__class__.__name__
                print step.success

        return steps_ok == len(self.steps)

    def run(self):
        if self.thread:
            Lib.instance().thread_register(("thread_%d" % self.thread.ident))

        for step in self.steps:
            step.run()
            if step.success == False:
                return False

        self.log(colored.green("+++ [%s] %d/%d steps completed successfully   +++"
                            % (self.name, len(self.steps), len(self.steps))))

        if self.account != None:
            self.account.delete()

    def run_background(self):
        self.thread = Thread(target=self.run, args=())
        self.thread.daemon = True
        self.thread.start()


