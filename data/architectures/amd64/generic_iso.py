kernel_flavor = "amd64-vyos"
bootloaders = "syslinux,grub-efi"
additional_repositories = [
    "deb [arch=amd64] https://repo.saltproject.io/py3/debian/10/amd64/3003 buster main",
    "deb [arch=amd64] http://repo.powerdns.com/debian bullseye-rec-45 main"
]

# Here you can copy/download/patch files for platform or make bootloader, etc. 
def _configure_hook(build_config: dict) -> None:
    import shutil
    shutil.copy(
        'data/architectures/amd64/package-lists/vyos-x86.list.chroot',
        'build/config/package-lists/'
    )

