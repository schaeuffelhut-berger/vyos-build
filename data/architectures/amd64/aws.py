from .generic_iso import *


def _configure_hook(build_config: dict) -> None:
    # run parent hook
    from . import generic_iso
    generic_iso._configure_hook(build_config)

    import os
    import shutil
    os.makedirs('build/config/includes.chroot/etc/cloud/cloud.cfg.d')
    shutil.copy('data/architectures/amd64/cloud-init/AWS/90_dpkg.cfg',
                'build/config/includes.chroot/etc/cloud/cloud.cfg.d/')
    shutil.copy('data/architectures/amd64/cloud-init/AWS/cloud-init.list.chroot',
                'build/config/package-lists/')
    shutil.copy('data/architectures/amd64/cloud-init/AWS/config.boot.default',
                'build/config/includes.chroot/opt/vyatta/etc/')
