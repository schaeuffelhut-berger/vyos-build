
# Debian configuration
debian_distribution = "bullseye"
debian_mirror = "http://deb.debian.org/debian"
debian_security_mirror = "http://deb.debian.org/debian"

# Custom vyos apt mirror
vyos_mirror = "http://dev.packages.vyos.net/repositories/current"

# vyos version information
release_train = "sagitta"
vyos_branch = "current"

# linux kernel version information
kernel_version = "5.10.77"

# ['release', 'development']
build_type = "development"

# custom linux packages to deploy in vyos image
custom_packages = []

custom_apt_key = []

def __get_default_built_by() -> str:
    import getpass
    import platform
    return "{user}@{host}".format(user=getpass.getuser(), host=platform.node())
build_by = __get_default_built_by()

