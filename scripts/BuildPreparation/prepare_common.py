import os
import shutil

from . import live_build_config
from . import make_version_file


def prepare(build_config: dict) -> None:
    """Copy the platform-independent live-build config files and run lb config."""
    if os.path.isdir('build/config/'):
        shutil.rmtree('build/config/')
    shutil.copytree('data/live-build-config/', 'build/config/')
    live_build_config.write(build_config)
    import_local_packages()
    make_version_file.make_version_file(build_config)
    if build_config['build_type'] == 'development':
        shutil.copy('data/package-lists/vyos-dev.list.chroot', 'build/config/package-lists/')

def import_local_packages() -> None:
    """Copy local packages into live-build path. """
    PKG_SRC_DIR = 'packages/'
    PKG_DST_DIR = 'build/config/packages.chroot/'
    if not os.path.isdir(PKG_DST_DIR):
        os.makedirs(PKG_DST_DIR)
    for file in [f for f in os.listdir(PKG_SRC_DIR) 
			if os.path.isfile(os.path.join(PKG_SRC_DIR, f))]:
        if file.endswith('.deb'):
            shutil.copy(os.path.join(PKG_SRC_DIR, file), PKG_DST_DIR)

