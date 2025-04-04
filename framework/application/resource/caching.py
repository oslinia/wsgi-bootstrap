import os

from .mapping import Mapper


def build_mask(items: list[tuple[int, tuple[str, ...]] | None]):
    if items is not None:
        mask = ''.join((f"        {num}: {masks},\n" for num, masks in items))

        return f"{{\n{mask}    }}"


def build_link(items: list[tuple[int, str, str]]):
    return ''.join((f"        {num}: ('{path}', r'{pattern}'),\n" for num, path, pattern in items))


def routing(mapper: Mapper):
    patterns, masks, links = (s if '' == s else f"\n{s}" for s in (
        ''.join((f"    (r'{pattern}', '{name}'),\n" for pattern, name in mapper.patterns)),
        ''.join((f"    '{name}': {build_mask(items)},\n" for name, items in mapper.masks.items())),
        ''.join((f"    '{name}': {{\n{build_link(items)}    }},\n" for name, items in mapper.links.items())),
    ))

    return (f"patterns = ({patterns})\n\n"
            f"masks = {{{masks}}}\n\n"
            f"links = {{{links}}}")


def slash(dirname: str, path: str, static: str, templates: str):
    def throw():
        if argument.startswith('/'):
            raise ValueError(f"Argument '{name}' must not begin with a slash: '{argument}'.")

        elif argument.endswith('/'):
            raise ValueError(f"Argument '{name}' must not end with a slash: '{argument}'.")

    for argument, name in (
            (path, 'static_urlpath'),
            (static, 'static_folder'),
            (templates, 'templates_folder'),
    ):
        throw()

    return ('/' if '' == path else f"/{path}/",
            os.path.realpath(f"{dirname}{os.sep}{static}"),
            os.path.realpath(f"{dirname}{os.sep}{templates}"))


def empty(lang: str, encoding: str):
    def throw():
        if '' == argument:
            raise ValueError(f"Argument '{name}' cannot be an empty string.")

    for argument, name in (
            (lang, 'templates_lang'),
            (encoding, 'encoding'),
    ):
        throw()

    return lang, encoding


def valid(dirname: str, path: str, static: str, lang: str, templates: str, encoding: str):
    return *slash(dirname, path, static, templates), *empty(lang, encoding)


def write(file: str, path: str, static: str, templates: str, lang: str, encoding: str):
    with open(file, 'w') as f:
        f.write(f"path = '{path}'\n\n"
                f"static = r'{static}'\n\n"
                f"encoding = '{encoding}'\n\n"
                f"lang = '{lang}'\n\n"
                f"templates = r'{templates}'\n\n"
                f"{routing(Mapper())}\n\n\n"
                f"def __dir__():\n"
                f"    return ['path', 'static', 'encoding', 'lang', 'templates', 'patterns', 'masks', 'links']\n")
