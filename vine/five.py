# -*- coding: utf-8 -*-
"""
    vine.five
    ~~~~~~~~~

    Compatibility implementations of features
    only available in newer Python versions.


"""
from __future__ import absolute_import, unicode_literals

import sys

PY3 = sys.version_info[0] == 3

# ############# Py3 <-> Py2 #################################################

if PY3:  # pragma: no cover
    string = str
    string_t = str
    long_t = int
    text_t = str

    def items(seq):
        return seq.items()

else:
    string = unicode                # noqa
    string_t = basestring           # noqa
    text_t = unicode
    long_t = long                   # noqa

    def items(seq):
        return seq.iteritems()


def with_metaclass(Type, skip_attrs={'__dict__', '__weakref__'}):
    """Class decorator to set metaclass.

    Works with both Python 2 and Python 3 and it does not add
    an extra class in the lookup order like ``six.with_metaclass`` does
    (that is -- it copies the original class instead of using inheritance).

    """

    def _clone_with_metaclass(Class):
        attrs = {key: value for key, value in items(vars(Class))
                 if key not in skip_attrs}
        return Type(Class.__name__, Class.__bases__, attrs)

    return _clone_with_metaclass
