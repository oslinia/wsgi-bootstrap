from framework.routing import Error, Rule, endpoint, Endpoint

from .endpoints import Handler, index, File, Page, Query, Archive

Error(Handler)

Rule('/', 'index')
Endpoint('index', endpoint(index))

Rule('/file/{name}', 'file'). \
    where(dict(name='[a-z.]+'))
Endpoint('file', endpoint(File))

Rule('/page/{name}', 'page'). \
    where(dict(name='[A-Za-z0-9._-]+'))
Endpoint('page', endpoint(Page))

Rule('/query', 'query')
Endpoint('query', endpoint(Query))

Rule('/archive/{year}', 'archive'). \
    where(dict(year='[0-9]{4}'))
Rule('/archive/{year}/{month}', 'archive')
Rule('/archive/{year}/{month}/{day}', 'archive'). \
    where(dict(year='[0-9]{4}', month='[0-9]{1,2}', day='[0-9]{1,2}'))
Endpoint('archive', endpoint(Archive))
