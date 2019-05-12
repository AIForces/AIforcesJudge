from importlib import import_module as _import_module
from os import path as _path
from os import listdir as _listdir

from .base_state import BaseState

_cur_dir = _path.dirname(_path.abspath(__file__))
_modules = list(
    map(
        lambda file: file[:-3],
        filter(
            lambda file: not file.startswith('__') and not file.startswith('.'),
            _listdir(_cur_dir)
        )
    )
)


for module in _modules:
    _import_module('.' + module, package='states')
