from .generic_iso import *


def _configure_hook(build_config: dict) -> None:
    # run parent hook
    from . import generic_iso
    generic_iso._configure_hook(build_config)

    import os
    import shutil
    os.makedirs('build/config/includes.chroot/etc/systemd/network')
    os.makedirs('build/config/includes.chroot/usr/share/initramfs-tools/hooks')
    shutil.copy('data/architectures/amd64/dell/90-vep.chroot', 'build/config/hooks/live/')
    for file in [f for f in os.listdir('data/architectures/amd64/dell/vep1400/') 
        if os.path.isfile(os.path.join('data/architectures/amd64/dell/vep1400/', f))]:
        if file.endswith('.link'):
            shutil.copy(
                os.path.join('data/architectures/amd64/dell/vep1400/', file),
                'build/config/includes.chroot/etc/systemd/network/'
            )
    shutil.copy('data/architectures/amd64/dell/vep-hook', 'build/config/includes.chroot/usr/share/initramfs-tools/hooks/')

