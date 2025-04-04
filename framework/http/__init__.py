from .wrapper import Any, http, Path, Http


def header(name: str, value: str):
    http.header.simple[name] = value


def has(name: str):
    return name in http.header.simple


def delete(name: str):
    if name in http.header.simple:
        del http.header.simple[name]


def query(name: str):
    return http.query.get(name)


def cookie(name: str):
    return http.cookie.get(name)


def form(name: str):
    return http.form.data.get(name)


def upload(name: str):
    return http.form.upload.get(name)


def charset(encoding: str):
    http.encoding = encoding


def media(file: str):
    return http.media(file)


def response(
        body: bytes | str,
        *,
        code: int = None,
        mimetype: str = None,
):
    return body, code, mimetype, http.encoding


def static(name: str):
    return http.static(name)


def link(*args: str, **kwargs: str):
    return http.link(args, kwargs)


def template(
        name: str,
        context: dict[str, Any] = None,
        *,
        code: int = None,
        mimetype: str = 'text/html',
):
    return http.template(name, context, code, mimetype, http.encoding)
