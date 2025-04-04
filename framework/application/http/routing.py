import re

from typing import Any

from ..resource import cache, Map
from ...http import Path


def static(name: str):
    return f"{cache.path}{name}"


def link(args: tuple[str, ...], kwargs: dict[str, str]):
    name, = args

    if cache.link.has(name):
        length, links = len(kwargs), cache.link.get(name)

        if length in links:
            mask, pattern = links[length]

            for k, v in kwargs.items():
                mask = mask.replace(f"{{{k}}}", v)

            if match := re.fullmatch(pattern, mask):
                return match.string


def convert(body: bytes | str, code: int = None, mimetype: str = None, encoding: str = None):
    kwargs = dict()

    if code is not None:
        kwargs.update(code=code)

    if mimetype is not None:
        kwargs.update(mimetype=mimetype)

    if encoding is not None:
        kwargs.update(encoding=encoding)

    return body, kwargs


class Callback(object):
    __slots__ = 'object', 'method', 'args', 'kwargs'

    def type(self, args: tuple[Any, ...], kwargs: dict[str, Any]):
        call = self.object(*args)

        if self.method is not None:
            call = getattr(call, self.method)

        return call(**kwargs)

    def __init__(self, module: str, name: str, method: str = None):
        self.object, self.method = getattr(__import__(module, fromlist=[name]), name), method

    def __call__(self, *args, **kwargs):
        match self.object.__class__.__name__:
            case 'type':
                call = self.type(args, kwargs)

            case _:
                call = self.object(*args, **kwargs)

        if isinstance(call, bytes | str):
            return convert(call)

        return convert(*call)


class Routing(Map):
    __slots__ = 'path',

    path: dict[str, str] | None

    def arguments(self, middleware: tuple[tuple[Any, ...], dict[str, Any]] | None):
        args, kwargs = tuple(), dict() if middleware is None else middleware

        if self.path is not None:
            kwargs.update(path=Path(self.path))

        return args, kwargs

    def endpoint(self, name: str):
        endpoint, middleware = self.endpoints[name]

        args, kwargs = self.arguments(middleware)

        return Callback(*endpoint)(*args, **kwargs)

    def route(self, name: str, values: str | tuple[str, ...]):
        self.path, masks = None, cache.masks[name]

        if masks is not None:
            if isinstance(values, str):
                values = values,

            num = len(values)

            if num in masks:
                self.path = dict(zip(masks[num], values))

        if name in self.endpoints:
            return self.endpoint(name)

    def response(self, path: str):
        callback = None

        for pattern, name in cache.patterns:
            if r := re.findall(pattern, path):
                callback = self.route(name, r[0])

                break

        if callback is None:
            if self.error is None:
                return convert(b'Not Found', 404, encoding='ascii')

            else:
                return Callback(*self.error)(code=404)

        return callback
