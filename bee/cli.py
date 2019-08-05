import functools
import os
import sys
from getpass import getpass
from os import path

from easycli import Root, SubCommand, Argument

from .configuration import settings, dump as dump_config, \
    initialize as initialize_settings
from .helpers import error, success
from .cache import cache
from .http import query


class Delete(SubCommand):
    __command__ = 'delete'
    __aliases__ = ['d']
    __arguments__ = [
        Argument(
            'list',
            default='',
            help='example: foo',
            completer=cache.getlists
        ),
        Argument(
            'item',
            help='Item to delete',
            completer=cache.getitems
        )
    ]

    def __call__(self, args):
        success(query('delete', f'{args.list}/{args.item}'))
        cache.refresh()


class Append(SubCommand):
    __command__ = 'append'
    __aliases__ = ['add', 'a']
    __arguments__ = [
        Argument(
            'list',
            default='',
            help='example: foo',
            completer=cache.getlists
        ),
        Argument(
            'item',
            help='Item to add',
            completer=cache.getitems
        )
    ]

    def __call__(self, args):
        success(query('append', f'{args.list}/{args.item}'))
        cache.refresh()


class Show(SubCommand):
    __command__ = 'show'
    __aliases__ = ['s', 'l']
    __arguments__ = [
        Argument(
            '-a', '--all',
            action='store_true',
            help='Get all action',
        ),
        Argument(
            'list',
            nargs='?',
            default='',
            help='example: foo',
            completer=cache.getlists
        )
    ]

    def __call__(self, args):
        success(query('get', 'all' if args.all else args.list))


class Info(SubCommand):
    __command__ = 'info'
    __aliases__ = ['i']

    def __call__(self, args):
        success(query('info'))
        cache.refresh()


class Login(SubCommand):
    __command__ = 'login'
    __arguments__ = [
        Argument('username', help='Username or email')
    ]
    def __call__(self, args):
        settings.token = query('login', form=dict(
            email=args.username,
            password=getpass()
        ))
        settings.username = args.username
        dump_config()


class Bee(Root):
    __help__ = 'Sharedlists client'
    __completion__ = True
    __arguments__ = [
        Login,
        Show,
        Info,
        Append,
        Delete,
    ]

    def main(self, argv=None):
        initialize_settings()
        return super().main(argv=argv)

    def __call__(self, args):
        success(query('get'))


