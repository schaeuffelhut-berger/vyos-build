import pkgutil as _pkgutil

# current module directory, then append the directory 'architectures', which
# is symlinked to data/architectures
__ARCH_PACKAGE_PATH = [__path__[0] + '/architectures']

class __ArchitectureModuleLoader():
    def __init__(self, architecture_path: str) -> None:
        self.__architecture_path = architecture_path
        self.arch_modules = []
        self.default_files = []

    def discover_modules(self) -> list:
        arch_modules = list(_pkgutil.walk_packages(self.__architecture_path))
        for module_info in arch_modules:
            module = module_info.module_finder.find_module(module_info.name).load_module(module_info.name)
            if module_info.ispkg:  # module is package (architecture folder)
                self.arch_modules.append(module)
            else:  # module is a platform-independent config file in the folder
                self.default_files.append(module)

# instanciate the ModuleLoader and let it find the arch submodules
__module_loader = __ArchitectureModuleLoader(__ARCH_PACKAGE_PATH)
__module_loader.discover_modules()

# set easily accessible variables for use in other modules
ARCH_MODULES = __module_loader.arch_modules
DEFAULT_MODULES = __module_loader.default_files
