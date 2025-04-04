import os
import sys

from . import cache
from .caching import valid, write
from .mapping import mapper, Link, Map


def import_module(import_name: str):
    dirname = os.path.dirname(file := sys.modules[import_name].__file__)

    if not file.endswith('.__init__py'):
        return f"{os.path.splitext(import_name)[0]}." if '.' in import_name else '', dirname

    return import_name, dirname


def initialize(import_name: str):
    import_name, dirname = import_module(import_name)

    file = f"{dirname}{os.sep}resource{os.sep}cache.py"

    return import_name, dirname, file, mapper(file, dirname, import_name)


def init(
        import_name: str,
        static_urlpath: str | None,
        static_folder: str | None,
        templates_lang: str | None,
        templates_folder: str | None,
        encoding: str | None,
):
    import_name, dirname, file, not_file = initialize(import_name)

    if not_file:
        directory = f"{dirname}{os.sep}resource"

        if not os.path.isdir(directory):
            os.mkdir(directory)

        write(file, *valid(dirname, *(d if a is None else a for a, d in (
            (static_urlpath, 'static'),
            (static_folder, 'static'),
            (templates_lang, 'en'),
            (templates_folder, 'templates'),
            (encoding, 'utf-8'),
        ))))

    module = __import__(f"{import_name}resource.cache", fromlist=['*'])

    for name in module.__dir__():
        match name:
            case 'links':
                setattr(cache, 'link', Link(getattr(module, name)))

            case _:
                setattr(cache, name, getattr(module, name))
