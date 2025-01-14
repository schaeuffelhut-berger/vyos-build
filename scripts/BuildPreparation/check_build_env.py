#!/usr/bin/env python3
#
# Copyright (C) 2015 VyOS maintainers and contributors
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 or later as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# File: check-build-env
# Purpose:
#   Checks if packages required for package and ISO image build
#   are installed.


import os
import sys

import util

deps = {
    'packages': [
       'sudo',
       'make',
       'live-build',
       'pbuilder',
       'devscripts',
       'python3-pystache',
       'python3-git'
    ],
   'binaries': []
}

def check():
    print("Checking if packages required for VyOS image build are installed")

    checker = util.DependencyChecker(deps)

    missing = checker.get_missing_dependencies()
    if not missing:
        print("All dependencies are installed")
        return(0)
    else:
        checker.print_missing_deps()
        return(1)


if __name__ == '__main__':
    retval = check()
    sys.exit(retval)
