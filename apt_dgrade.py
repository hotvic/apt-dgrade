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

import argparse

try:
    import apt
    import apt.progress
    import apt_pkg
except ImportError:
    print "Error: cannot find required python libraries: apt, apt.progress, apt_pkg; one or several of these."
    print "Please install these libraries then re-run this program."
    print "On Debian the package of these libraries is called: python-apt"
