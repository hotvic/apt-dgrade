#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-
#
# Copyright © 2013 Victor Aurélio <victoraur.santos@gmail.com>
#
# This file is part of apt-dgrade.
#
# apt-dgrade is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# apt-dgrade is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with apt-dgrade.  If not, see <http://www.gnu.org/licenses/>.

import json as _json
import gettext as _gettext

MESSAGES_FILE = "locale/messages.json"

class MessageError(Exception):
    pass


class InvalidMessage(MessageError):
    def __init__(self, message):
        self._message = message

    def __str__(self):
        return "Invalid message, {0} doesn't exist".format(self._message)


class Message(object):
    """ This class manage the messages in MESSAGES_FILE file.

    Is unicode and i18n compatible"""
    def __init__(self, domain=None):
        """ Initialize the Message class

        Keyword arguments:
        domain -- the gettext domain, None disable gettext (default None)

        """
        self._inter = False
        with open(MESSAGES_FILE) as f:
            self._json = _json.load(f)
        if not domain is None:
            self._t = _gettext.translation(domain)
            self._ = self._t.gettext
            self._inter = True

    def show(self, message, **kargs):
        """ Print a message to stdout

        Positional arguments:
        message -- message to show

        Keyword arguments:
        **kargs -- arguments to replace in string

        """
        if not message in self._json:
            raise InvalidMessage
        if self._inter:
            if len(kargs) > 0:
                print self._(self._json[messa]) % kargs
            else:
                print self._(self._json[message])
        else:
            if len(kargs) > 0:
                print self._json[message] % kargs
            else:
                print self._json[message]

    def get(self, message, **kargs):
        """ Return a string (message) optionally formated (see below)

        Positional arguments:
        message -- the message title to get

        Keyword arguments:
        **kargs -- arguments to replace in  string, if not passed
                   the string isn't replaced

        """
        if not message in self._json:
            raise InvalidMessage
        if self._inter:
            if len(kargs) > 0:
                return self._(self._json[messa]) % kargs
            else:
                return self._(self._json[message])
        else:
            if len(kargs) > 0:
                return self._json[message] % kargs
            else:
                return self._json[message]
