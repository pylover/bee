import sys
import functools


error = functools.partial(print, file=sys.stderr)
success = functools.partial(print, end='')

