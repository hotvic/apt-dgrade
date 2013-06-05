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

import  argparse

import message

try:
    import apt
    import apt.progress
    import apt_pkg
except ImportError:
    print "Error: cannot find required python libraries: apt, apt.progress, " \
        "apt_pkg; one or several of these."
    print "Please install these libraries then re-run this program."
    print "On Debian the package of these libraries is called: python-apt"


class AptDgrade(object):
    def __init__(self, opts):
        if not hasattr(opts, 'root'):
            self._cache = apt.cache.Cache()
        else:
            self._cache = apt.cache.Cache(opts.root)
        self._opts = opts

    def yesno(self, prompt, yes=False):
        if self._opts.yes_all:
            return True
        elif not self._opts.yes_all and self._opts.yes and yes:
            return True
        else:
            while True:
                rin = raw_input(prompt)
                if not rin:
                    return yes
                elif "yes".startswith(rin.lower()):
                    return True
                elif "no".startswith(rin.lower()):
                    return False
                else:
                    msg.show('invalid_response')

    def pick_origin(self, pkgver):
        return pkgver.origins[0]

    def search(self):
        for pkg in self._cache:
            if pkg.installed and not pkg.candidate.downloadable:
                cand = None
                for ver in pkg.versions:
                    if ver.downloadable:
                        cand = ver
                if cand is None:
                    args = {'name': pkg.name,
                            'pkgver': pkg.installed.version
                            }
                    if self.yesno(msg.get('Qremove', **args), True):
                        pkg.mark_delete()
                else:
                    args = {'name': pkg.name,
                            'pkgver': pkg.installed.version,
                            'candver': cand.version,
                            'archive': self.pick_origin(cand).archive
                            }
                    if yesno(msg.get('Qforce', **args), True):
                        pkg.candidate = cand
                        pkg.mark_install(auto_fix=False, auto_inst=True,
                            from_user=False)

    def commit(self):
        if not self._opts.force:
            apt.cache.ProblemResolver(self._cache).resolve()
        if not self._cache.get_changes():
            msg.show('system_ok')
            return
        else:
            msg.show('changes_made"')
            for pkg in cache.get_changes():
                print "  {0} {1} => {2} ({3})".format(pkg.name,
                    pkg.installed.version, None if pkg.marked_delete
                        else pkg.candidate.version, self.pick_origin(
                            pkg.candidate).archive)
            msg.show('download_size', bytes=cache.required_download/1e6)
            if self.yesno(msg.get('Qmake_changes')):
                while True:
                    try:
                        cache.commit(apt.progress.text.AquirePorgress(),
                                apt.progress.base.InstallProgress())
                    except SystemError as e:
                        print e
                        if not self.yesno(msg.get('Qtry_again'), True):
                            raise SystemError(100)
                        continue
                    else:
                        break
            else:
                msg.show('operation_cancelled')

msg = message.Message()
parser = argparse.ArgumentParser(prog="apt-dgrade",
        description=msg.get('description'))
# Add arguments
parser.add_argument("--force", "-f", action="store_true",
        help=msg.get('help_force'))
parser.add_argument("--update", "-u", action="store_true",
        help=msg.get('help_update'))
parser.add_argument("--yes", "-y", action="store_true",
        help=msg.get('help_yes'))
parser.add_argument("--yes-all", "-yy", action="store_true",
        help=msg.get('help_yes_all'))

args = parser.parse_args()

dgrade = AptDgrade(args)
dgrade.search()
dgrade.commit()
