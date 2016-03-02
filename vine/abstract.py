from __future__ import absolute_import, unicode_literals

import abc

from collections import Callable

from .five import with_metaclass

__all__ = ['Thenable']


@with_metaclass(abc.ABCMeta)
class Thenable(Callable):  # pragma: no cover
    __slots__ = ()

    @abc.abstractmethod
    def then(self, on_success, on_error=None):
        raise NotImplementedError()

    @abc.abstractmethod
    def throw(self, exc=None):
        raise NotImplementedError()

    @abc.abstractmethod
    def cancel(self):
        raise NotImplementedError()

    @classmethod
    def __subclasshook__(cls, C):
        if cls is Thenable:
            if any('then' in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented
