"""Promises, promises, promises"""
from __future__ import absolute_import

from .abstract import Thenable
from .promises import promise
from .synchronization import barrier
from .funtools import (
    maybe_promise, ensure_promise,
    ppartial, preplace, starpromise, transform, wrap,
)

VERSION = (0, 9, 0)
__version__ = '.'.join(map(str, VERSION[0:3])) + ''.join(VERSION[3:])
__author__ = 'Ask Solem'
__contact__ = 'celery@celeryproject.org'
__homepage__ = 'http://github.com/celery/vine'
__docformat__ = 'restructuredtext'

# -eof meta-

__all__ = [
    'Thenable', 'promise', 'barrier',
    'maybe_promise', 'ensure_promise',
    'ppartial', 'preplace', 'starpromise', 'transform', 'wrap',
]
