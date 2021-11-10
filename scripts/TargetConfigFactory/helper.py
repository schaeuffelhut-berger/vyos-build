import types
import TargetConfigFactory


class ConfigGenerator:
    """Class for storing, handling and building platform specific build configs. """

    def __init__(self):
        self.__config_cache = None

    def __getitem__(self, key: str) -> object:
        """Config items should be accessible via config['key']. """
        if self.__config_cache is None:
            self.rebuild_default_config()
        if key not in self.__config_cache:
            print(self.__config_cache)
            raise KeyError('Config option \'{}\' not found in any loaded config! '.format(key))
        return self.__config_cache[key]

    def __setitem__(self, key: str, value: object) -> None:
        """Config items should be settable via config['key'] = value. """
        self.__config_cache[key] = value

    def __contains__(self, key: str) -> bool:
        return key in self.__config_cache

    def to_dict(self) -> dict:
        """Export all current config options to a dict. """
        return self.__config_cache.copy()

    def merge(self, data: dict, priority: bool) -> None:
        """Merge config options from a given dict into the local config cache. """
        # keys only found in given data, copy to config cache if not None
        for key in (set(data.keys()) - set(self.__config_cache.keys())):
            if data[key] is not None:
                self.__config_cache[key] = data[key]

        # merge conflicts
        # -> always append if type is list
        # -> overwrite local if priority is set
        for key in (set(data.keys()).intersection(set(self.__config_cache.keys()))):
            if data[key] is None:
                continue

            if type(data[key]) == list and type(self.__config_cache[key]) == list:
                data[key] += self.__config_cache[key]
            elif priority:
                self.__config_cache[key] = data[key]

    def apply_module(self, module: types.ModuleType) -> None:
        """Get all declared variables within module scope and update local config cache with it. """
        self.__config_cache.update({
            k: v
            for k, v in module.__dict__.items()
            if not k.startswith('_')
        })

    def rebuild_default_config(self) -> None:
        """Parse all platform-independent config files in alphabetical order and load their config options. """
        self.__config_cache = {}
        module_by_name = {mod.__name__: mod for mod in TargetConfigFactory.DEFAULT_MODULES}
        # Sorting _here_ is a very important part of this configuration builder.
        # This makes sure that a config option defined in '20_xxx.py' has priority over '10_xxx.py'.
        for module_name in sorted(module_by_name.keys()):
            self.apply_module(module_by_name[module_name])


# Instanciate the config generator and save in module scope.
# Use this object in configure script when interacting with config.
config = ConfigGenerator()
# walk platform-independent modules and read their values
config.rebuild_default_config()


def get_available_target_tree() -> 'dict[str, list[str]]':
    """Get all available architectures and their targets and return them in a dict. 
    Example: {
        'arm64': ['generic_iso', 'raspberry_pi_cm4', 'raspberry_pi_3b'],
        'amd64': ['generic_iso'],
    }
    """
    return {
        mod.__name__: [
            attribute for attribute in mod.__dict__.keys()
            if not attribute.startswith('_')
        ]
        for mod in TargetConfigFactory.ARCH_MODULES
    }


def load_architecture(arch: str, target: str) -> types.ModuleType:
    """Load a given architecture and target combination by their names and apply their configuration. """
    module_by_name = {mod.__name__: mod for mod in TargetConfigFactory.ARCH_MODULES}
    assert arch in module_by_name, \
        'Tried to load architecture \'{}\', but it the package cannot be found!'.format(arch)
    assert hasattr(module_by_name[arch], target), \
        'Configuration target not found for architecture \'{}\'. Please make sure the package has the ' \
        'attribute \'{}\' defined in the architecture-module\'s __init__.py! '.format(arch, target)
    target_module = getattr(module_by_name[arch], target)
    config.apply_module(target_module)
    return target_module

