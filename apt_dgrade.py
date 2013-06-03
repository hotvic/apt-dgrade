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
    def __init__(self, opts, root=None):
        self._cache = apt.cache.Cache(rootdir=root)
        self._opts = opts

    def yesno(prompt, yes=False):
        if self._opts.yes_all:
            return True
        elif not self._opts.yes_all and self._opts.yes and yes:
            return True
        else:
            while True:
                rin = raw_input(prompt)
                if not rin:
                    return yes
                elif "yes".startwith(rin.lower()):
                    return True
                elif "no".startwith(rin.lower()):
                    return False
                else:
                    print "Invalid response! Valid responses are: yes, no, y, n"

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
                    prompt = "Remove {0} version {1} [y]? ".format(pkg.name,
                        pkg.installed.version)
                    if self.yesno(prompt, True):
                        pkg.mark_delete()
                else:
                    prompt = "Force '{0}' version\n  from {1}\n  to   {2} "\
                        "({3}) [y]? ".format(pkg.name, pkg.installed.version,
                            cand.version, self.pick_origin(cand).archive))
                    if yesno(prompt, True):
                        pkg.candidate = cand
                        pkg.mark_install(auto_fix=False, auto_inst=True,
                            from_user=False)

    def commit(self):
        if not self._opts.force:
            apt.cache.ProblemResolver(case).resolve()
        if not self._cache.get_changes():
            print "Congratulations! Your system is OK"
            return
        else:
            prompt = "Do you wish to make the changes above [n] ?"
            print "The following changes will be made..."
            for pkg in cache.get_changes():
                print "  {0} {1} => {2} ({3})".format(pkg.name,
                    pkg.installed.version, None if pkg.marked_delete
                        else pkg.candidate.version, self.pick_origin(
                            pkg.candidate).archive)
            print "{0.1f} MB will be downloaded".format(
                cache.required_download/1e6)
            if self.yesno(prompt, False):
                while True:
                    try:
                        cache.commit(apt.progress.text.AquirePorgress(),
                            apt.progress.base.InstallProgress())
                    except SystemError as e:
                        prompt = "An error ocurred, try again [y] ?"
                        print e
                        if not self.yesno(prompt, True):
                            raise SystemError(100)
                        continue
                    else:
                        break
            else:
                print "Operation cancelled by user."

parser = argparse.ArgumentParser(
    prog="apt-dgrade",
    description="An utility to help you to downgrade your debian or " \
        "debian-based system to packages in the active repositories")
# Add arguments
parser.add_argument("--force", "-f", action="store_true",
    help="Force requested changes, don't resolve problems")
parser.add_argument("--update", "-u", action="store_true",
    help="Update the package cache first")
parser.add_argument("--yes", "-y", action="store_true",
    help="Assume yes to all questions which yes is the default")
parser.add_argument("--yes-all", "-yy", action="store_true",
    help="Assume yes to all questions")

args = parser.parse_args()

dgrade = AptDgrade()
dgrade.search()
dgrade.commit()
