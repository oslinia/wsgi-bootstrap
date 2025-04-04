from typing import Any

from ..application import http


class Path(dict[str, str]):
    def __init__(self, tokens: dict[str, str]):
        super().__init__(tokens)


class Http(object):
    __slots__ = 'http',

    def __init__(self):
        self.http = http

    def header(self, name: str, value: str):
        self.http.header.simple[name] = value

    def has(self, name: str):
        return name in self.http.header.simple

    def delete(self, name: str):
        if name in self.http.header.simple:
            del self.http.header.simple[name]

    def query(self, name: str):
        return self.http.query.get(name)

    def cookie(self, name: str):
        return self.http.cookie.get(name)

    def form(self, name: str):
        return self.http.form.data.get(name)

    def upload(self, name: str):
        return self.http.form.upload.get(name)

    def charset(self, encoding: str):
        self.http.encoding = encoding

    def media(self, file: str):
        return self.http.media(file)

    def response(
            self,
            body: bytes | str,
            *,
            code: int = None,
            mimetype: str = None,
    ):
        return body, code, mimetype, self.http.encoding

    def static(self, name: str):
        return self.http.static(name)

    def link(self, *args: str, **kwargs: str):
        return self.http.link(args, kwargs)

    def template(
            self,
            name: str,
            context: dict[str, Any] = None,
            *,
            code: int = None,
            mimetype: str = 'text/html',
    ):
        return self.http.template(name, context, code, mimetype, self.http.encoding)
