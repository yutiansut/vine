
import abc

from collections import Callable

__all__ = ['Thenable']


class Thenable(Callable, metaclass=abc.ABCMeta):  # pragma: no cover
    __slots__ = ()

    @abc.abstractmethod
    def then(self, on_success, on_error=None):
        ...

    @abc.abstractmethod
    def throw(self, exc=None, tb=None, propagate=True):
        ...

    @abc.abstractmethod
    def cancel(self):
        ...

    @classmethod
    def __subclasshook__(cls, C):
        if cls is Thenable:
            if any('then' in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented


@Thenable.register
class ThenableProxy:

    def _set_promise_target(self, p):
        self._p = p

    def then(self, on_success, on_error=None):
        return self._p.then(on_success, on_error)

    def cancel(self):
        return self._p.cancel()

    def throw1(self, exc=None):
        return self._p.throw1(exc)

    def throw(self, exc=None, tb=None, propagate=True):
        return self._p.throw(exc, tb=tb, propagate=propagate)

    @property
    def cancelled(self):
        return self._p.cancelled

    @property
    def ready(self):
        return self._p.ready

    @property
    def failed(self):
        return self._p.failed
