kernel_flavor = "v8-arm64-vyos"
bootloaders = "grub-efi"
additional_repositories = [
    "deb [arch=arm64] https://repo.saltproject.io/py3/debian/11/arm64/3004 bullseye main"
]


# Here you can copy/download/patch files for platform or make bootloader, etc. 
def _configure_hook(build_config: dict) -> None:
    pass

