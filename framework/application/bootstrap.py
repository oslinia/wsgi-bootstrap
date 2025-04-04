import os

from collections.abc import Generator
from datetime import datetime, timezone
from io import DEFAULT_BUFFER_SIZE
from typing import Any
from zoneinfo import ZoneInfo

from . import StartResponse, Environment, Application
from .http.call import Head, Media, Response
from .http.call.response import Http
from .resource import cache, init
from ..utils import utc


class Bootstrap(object):
    __slots__ = 'path', 'static'

    def file(self, path: str):
        if path.startswith(self.path):
            file = f"{self.static}{os.sep}{path[len(self.path):]}"

            if os.path.isfile(file):
                return file

    def __init__(
            self: Application,
            import_name: str,
            static_urlpath: str = None,
            static_folder: str = None,
            templates_lang: str = None,
            templates_folder: str = None,
            encoding: str = None,
            time_zone: str = None,
    ):
        init(import_name, static_urlpath, static_folder, templates_lang, templates_folder, encoding)

        self.path = cache.path
        self.static = cache.static

        Http.encoding = cache.encoding
        Http.block_size = DEFAULT_BUFFER_SIZE

        utc.tz = timezone.utc if time_zone is None else ZoneInfo(time_zone)

    def __call__(self, environ: Environment, start_response: StartResponse) -> Generator[bytes, Any, None]:
        utc.now = datetime.now(timezone.utc)
        utc.timestamp = utc.now.timestamp()

        Head.cookie = dict()
        Head.simple = dict()

        file = self.file(environ['PATH_INFO'])

        if file is not None:
            return Media(file)(start_response)

        else:
            return Response(environ)(start_response)
