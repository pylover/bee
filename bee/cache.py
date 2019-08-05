import os
from itertools import groupby
from os import path

from .http import query

CACHEPATH = path.join(os.environ['HOME'], '.cache', 'bee')
CACHEFILE = path.join(CACHEPATH, 'items')

class Cache:
    dirty = False
    lists = []
    items = []

    def __init__(self):
        self.loadfromfile()

    def loadfromfile(self):
        if not path.exists(CACHEFILE):
            os.makedirs(path.dirname(CACHEFILE), exist_ok=True)
            return

        with open(CACHEFILE) as f:
            self.items = sorted(
                [i.strip().split('/', 1) for i in f.readlines()]
            )

            self.lists = list(i[0] for i in groupby(self.items, lambda x: x[0]))

    def refresh(self):
        with open(CACHEFILE, 'w') as f:
            data = query('get', 'all')
            f.write(data)

        self.loadfromfile()
        self.dirty = False

    def invalidate(self):
        self.dirty = True

    def ensure(self):
        if self.dirty:
            self.refresh()

    def getlists(self, **kw):
        return self.lists

    def getitems(self, prefix, action, parser, parsed_args):
        list_ = parsed_args.list
        if not list_:
            return (i[1] for i in self.items)

        return (i[1] for i in self.items if i[0] == list_)


cache = Cache()


