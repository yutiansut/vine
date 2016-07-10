"""Promises, promises, promises"""

import re

from typing import NamedTuple

from .funtools import (
    maybe_promise, ensure_promise,
    ppartial, preplace, starpromise, transform, wrap,
)
from .promises import promise
from .synchronization import barrier
from .types import Thenable

__version__ = '1.1.1'
__author__ = 'Ask Solem'
__contact__ = 'ask@celeryproject.org'
__homepage__ = 'http://github.com/celery/vine',
__docformat__ = 'restructuredtext'

# -eof meta-

version_info_t = NamedTuple('version_info_t', [
    ('major', int),
    ('minor', int),
    ('micro', int),
    ('releaselevel', str),
    ('serial', str),
])
# bump version can only search for {current_version}
# so we have to parse the version here.
_temp = re.match(
    r'(\d+)\.(\d+).(\d+)(.+)?', __version__).groups()
VERSION = version_info = version_info_t(
    int(_temp[0]), int(_temp[1]), int(_temp[2]), _temp[3] or '', '')
del(_temp)
del(re)

__all__ = [
    'Thenable', 'promise', 'barrier',
    'maybe_promise', 'ensure_promise',
    'ppartial', 'preplace', 'starpromise', 'transform', 'wrap',
]
