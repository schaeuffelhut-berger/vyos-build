#!/usr/bin/env python3
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
# File: live-build-config
# Purpose:
#   Creates a live-build config command from template using the build config
#   and executes it, to prepare the system for building the installation ISO.


import sys
import os
import shutil
import json
import subprocess

import defaults
import util

def write(build_config: dict) -> None:

    util.check_build_config()

    lb_arguments = {
        "architectures": build_config['build_architecture'],
        "bootappend-live": "boot=live components hostname=vyos username=live nopersistence noautologin nonetworking union=overlay console=ttyS0,115200 console=tty0 net.ifnames=0 biosdevname=0",
        "bootappend-live-failsafe": "live components memtest noapic noapm nodma nomce nolapic nomodeset nosmp nosplash vga=normal console=ttyS0,115200 console=tty0 net.ifnames=0 biosdevname=0",
        "linux-flavours": build_config['kernel_flavor'],
        "linux-packages": 'linux-image-{}'.format(build_config['kernel_version']),
        "bootloader": build_config['bootloaders'],
        "binary-images": 'iso-hybrid',
        "checksums": 'sha256 md5',
        "debian-installer": 'none',
        "distribution": build_config['debian_distribution'],
        "iso-application": "VyOS",
        "iso-publisher": build_config['build_by'],
        "iso-volume": "VyOS",
        "debootstrap-options": "--variant=minbase --exclude=isc-dhcp-client,isc-dhcp-common,ifupdown --include=apt-utils,ca-certificates,gnupg2",
        "mirror-bootstrap": build_config['debian_mirror'],
        "mirror-chroot": build_config['debian_mirror'],
        "mirror-chroot-security": build_config['debian_security_mirror'],
        "mirror-binary": build_config['debian_mirror'],
        "mirror-binary-security": build_config['debian_security_mirror'],
        "archive-areas": 'main contrib non-free',
        "firmware-chroot": 'false',
        "firmware-binary": 'false',
        "updates": 'true',
        "security": 'false',
        "backports": 'false',
        "utc-time": 'true',
        "apt-recommends": 'false',
        "apt-options": '--yes -oAPT::Get::allow-downgrades=true',
        "apt-indices": 'false',
        "debug": None,
    }

    debug = build_config['debug']

    # Add the additional repositories to package lists
    print("Setting up additional APT entries")
    vyos_repo_entry = "deb {0} {1} main\n".format(build_config['vyos_mirror'], build_config['vyos_branch'])

    apt_file = os.path.join(build_config['build_dir'], defaults.VYOS_REPO_FILE)

    if debug:
        print("Adding these entries to {0}:".format(apt_file))
        print("\t", vyos_repo_entry)

    with open(apt_file, 'w') as f:
        f.write(vyos_repo_entry)

    # Add custom APT entries
    if build_config['additional_repositories']:
        custom_apt_file = os.path.join(build_config['build_dir'], defaults.CUSTOM_REPO_FILE)
        entries = "\n".join(build_config['additional_repositories'])
        if debug:
            print("Adding custom APT entries:")
            print(entries)
        with open(custom_apt_file, 'w') as f:
            f.write(entries)
            f.write("\n")

    # Add custom APT keys
    if build_config['custom_apt_key']:
        key_dir = os.path.join(build_config['build_dir'], defaults.ARCHIVES_DIR)
        for k in build_config['custom_apt_key']:
            dst_name = '{0}.key.chroot'.format(os.path.basename(k))
            shutil.copy(k, os.path.join(key_dir, dst_name))

    # Add custom packages
    if build_config['custom_packages']:
        package_list_file = os.path.join(build_config['build_dir'], defaults.CUSTOM_PACKAGE_LIST_FILE)
        packages = "\n".join(build_config['custom_packages'])
        with open (package_list_file, 'w') as f:
            f.write(packages)

    # Configure live-build

    print("Configuring live-build")

    lb_config_command = ['lb', 'config', 'noauto']

    # add arguments as individual list items in order to avoid argument-splitting
    for key, value in lb_arguments.items():
        lb_config_command.append('--{}'.format(key))
        if value is not None:
            lb_config_command.append(value)

    result = subprocess.call(lb_config_command, cwd=defaults.BUILD_DIR)
    if result > 0:
        print("live-build config failed")
        sys.exit(1)


if __name__ == '__main__':
    with open(defaults.BUILD_CONFIG, 'r') as f:
        build_config = json.load(f)
        write(build_config)
