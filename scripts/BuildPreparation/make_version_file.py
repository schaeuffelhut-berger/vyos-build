#!/usr/bin/python3
#
# Copyright (C) 2018 VyOS maintainers and contributors
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
# File: make-version-file
# Purpose:
#   Creates version file in live-build chroot includes dir
#   that is included in the image and used by 'show version' command
#   and install/upgrade scripts.

import os
import datetime
import json
import uuid

import git

import defaults
import util


def make_version_file(build_config):

    # Create a build timestamp
    now = datetime.datetime.today()
    build_timestamp = now.strftime("%Y%m%d%H%M")

    # FIXME: use aware rather than naive object
    build_date = now.strftime("%a %d %b %Y %H:%M UTC")

    # Assign a (hopefully) unique identifier to the build (UUID)
    build_uuid = str(uuid.uuid4())

    # Initialize Git object from our repository
    try:
        repo = git.Repo('.')

        # Retrieve the Git commit ID of the repository, 14 charaters will be sufficient
        build_git = repo.head.object.hexsha[:14]
        # If somone played around with the source tree and the build is "dirty", mark it
        if repo.is_dirty():
            build_git += "-dirty"

        # Retrieve git branch name
        git_branch = repo.active_branch.name
    except Exception as e:
        print("Could not retrieve information from git: {0}".format(str(e)))
        build_git = ""
        git_branch = ""
        git_commit = ""

    # Create a build version
    if build_config['build_type'] == 'development':
        try:
            if not git_branch:
                raise ValueError("git branch could not be determined")

            # Load the branch to version mapping file
            with open('data/versions') as f:
                version_mapping = json.load(f)

            branch_version = version_mapping[git_branch]

            version = "{0}-rolling-{1}".format(branch_version, build_timestamp)
        except Exception as e:
            print("Could not build a version string specific to git branch, falling back to default: {0}".format(str(e)))
            version = "999.{0}".format(build_timestamp)
    else:
        # Release build, use the version from ./configure arguments
        version = build_config['version']

    if build_config['build_type'] == 'development':
        lts_build = False
    else:
        lts_build = True

    version_data = {
        'version': version,
        'built_by': build_config['build_by'],
        'built_on': build_date,
        'build_uuid': build_uuid,
        'build_git': build_git,
        'build_branch': git_branch,
        'release_train': build_config['release_train'],
        'lts_build': lts_build,
        'build_comment': build_config['build_comment']
    }

    os_release = f"""
    PRETTY_NAME="VyOS {version} ({build_config['release_train']})"
    NAME="VyOS"
    VERSION_ID="{version}"
    VERSION="{version} ({build_config['release_train']})"
    VERSION_CODENAME=bullseye
    ID=vyos
    HOME_URL="https://vyos.io"
    SUPPORT_URL="https://support.vyos.io"
    BUG_REPORT_URL="https://phabricator.vyos.net"
    """

    os.makedirs(os.path.join(defaults.CHROOT_INCLUDES_DIR, 'usr/share/vyos'), exist_ok=True)
    with open(os.path.join(defaults.CHROOT_INCLUDES_DIR, 'usr/share/vyos/version.json'), 'w') as f:
        json.dump(version_data, f)

    # For backwards compatibility with 'add system image' script from older versions
    # we need a file in the old format so that script can find out the version of the image
    # for upgrade
    os.makedirs(os.path.join(defaults.CHROOT_INCLUDES_DIR, 'opt/vyatta/etc/'), exist_ok=True)
    with open(os.path.join(defaults.CHROOT_INCLUDES_DIR, 'opt/vyatta/etc/version'), 'w') as f:
        print("Version: {0}".format(version), file=f)

    # Leaky abstraction: we want ISO file name include version number,
    # but we probably don't want to  have a separate build step just for this,
    # neither we want to use lengthy paths in makefiles
    with open(os.path.join(defaults.BUILD_DIR, 'version'), 'w') as f:
        print(version, file=f)

    # Define variables that influence to welcome message on boot
    os.makedirs(os.path.join(defaults.CHROOT_INCLUDES_DIR, 'usr/lib/'), exist_ok=True)
    with open(os.path.join(defaults.CHROOT_INCLUDES_DIR, 'usr/lib//os-release'), 'w') as f:
        print(os_release, file=f)


if __name__ == '__main__':
    # Load the build config
    util.check_build_config()
    with open(defaults.BUILD_CONFIG, 'r') as f:
        build_config = json.load(f)
        make_version_file(build_config)

