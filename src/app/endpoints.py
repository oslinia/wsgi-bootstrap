import os.path

from framework.http import header, charset, media, response, Path, Http
from framework.utils import utc


class Handler(Http):
    __slots__ = ()

    def __call__(self, code: int):
        self.charset('ascii')

        return self.response(f"Error: {code}", code=code)


def index():
    charset('ascii')
    header('head', 'Value')
    print(utc.now, utc.timestamp)

    return response('Index')


class File(object):
    __slots__ = 'static',

    def __init__(self):
        self.static = f"{os.path.dirname(__file__)}{os.sep}static{os.sep}"

    @property
    def not_found(self):
        return 'File not found!', 404

    def __call__(self, path: Path):
        file = f"{self.static}{path.get('name')}"

        return media(file)


class Page(Http):
    __slots__ = ()

    def __call__(self, path: Path):
        print(self.static('style.css'))
        print(self.link('index'))
        print(self.link('query'))
        print(self.link('error'))
        print(self.link('page', name='index.html'))
        print(self.link('archive', year='2025', month='02', day='23', error='23'))
        print(self.link('archive', year='2025', month='02', error='23'))
        print(self.link('archive', year='2025', month='02', day='23'))
        print(self.link('archive', year='2025', month='02'))
        # charset('ascii')
        # return self.response(f"page/{path['name']}")

        name = path['name']

        return self.template(f"page/{path['name']}", dict(title=f"PAGE {name[:-5]}", name=name))


class Query(Http):
    __slots__ = ()

    def __call__(self):
        return self.response(f"Query: {self.query('query')} {self.query('key')}")


class Archive(Http):
    __slots__ = ()

    def __call__(self, path: Path):
        self.charset('ascii')
        # charset('ascii')
        self.header('head', 'Archive')

        return self.response(f"Archive {path}")
