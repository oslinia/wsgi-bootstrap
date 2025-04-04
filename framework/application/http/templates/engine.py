import re

from typing import Any

from ...resource import cache


def init(context: dict[str, Any] | None):
    html: dict[str, Any] = {
        'lang': cache.lang,
    }

    if context is not None:
        html.update(context)

    return html


def string(value: str, args: tuple[str, ...]):
    for arg in args:
        value = getattr(value, arg)()

    return value


class Engine(object):
    __slots__ = 'context', 'args'

    def __init__(self, context: dict[str, Any] | None):
        self.context = init(context)

    @property
    def static(self):
        return f"{cache.path}{self.args.strip(r'\'"')}"

    @property
    def link(self):
        name, *args = (v.lstrip() if '=' in v else v.strip(r'\'"') for v in self.args.split(','))

        if cache.link.has(name):
            length, links = len(args), cache.link.get(name)

            if length in links:
                mask, pattern = links[length]

                for k, v in (a.split('=') for a in args):
                    mask = mask.replace(f"{{{k}}}", v.strip(r'\'"'))

                if match := re.fullmatch(pattern, mask):
                    return match.string

    def __call__(self, fragment: str):
        value, name, *args = None, *(e.strip() for e in re.split(r'\|', fragment[2:-2]))

        if '(' in name:
            method, self.args = (e.strip() for e in name[:-1].split('('))

            if method in ('static', 'link'):
                value = getattr(self, method)

        if name in self.context:
            return string(self.context[name], args)

        return '' if value is None else value
