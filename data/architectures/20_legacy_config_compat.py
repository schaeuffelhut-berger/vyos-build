
def _scope_wrapper():
    import json as _json
    import os.path as _path

    if _path.isfile('data/defaults.json'):
        print('=' * 80)
        print('Warning! Legacy config compat layer active, because there is a defaults.json in \'data/\' !')
        print('Please update your configuration to a python module. ')
        print('See documentation at https://<tbd>')
        print('=' * 80)

        config = _json.load(open('data/defaults.json', 'r'))
        globals().update(config)
        globals()['MAGIC_VALUE_DO_NOT_LOAD_ARCH'] = True

_scope_wrapper()

