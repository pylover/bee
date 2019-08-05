import requests

from .configuration import settings
from .helpers import error


def query(verb, path='/', form=None):
    kw = {}
    headers = {}
    if settings.token:
        headers['Authorization'] = settings.token

    if form:
        kw['data'] = form

    kw['verify'] = settings.sslverify
    kw['headers'] = headers
    response = requests.request(
        verb.upper(),
        f'{settings.url}/{path}',
        **kw
    )

    if response.status_code != 200:
        error(response.status_code, response.reason, '')
        return ''

    return response.text



