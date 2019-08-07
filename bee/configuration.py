import os
import functools
from os import path

from pymlconf import DeferredRoot


CONFIGFILE = path.join(os.environ['HOME'], '.beerc')
BUILTINSETTINGS = '''
  url: http://localhost:5555
  sslverify: true
  username:
  token:
'''

def dump():
    with open(CONFIGFILE, 'w') as f:
        f.write(settings.dumps())


settings = DeferredRoot()
def initialize():
    settings.initialize(BUILTINSETTINGS)
    if not path.exists(CONFIGFILE):
        dump()
    else:
        settings.load_file(CONFIGFILE)


