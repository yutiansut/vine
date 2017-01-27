import abc
import collections
from types import TracebackType
from typing import Any, Callable, Optional, TypeVar

__all__ = ['PromiseArg', 'Thenable', 'ThenableProxy']

PromiseArg = TypeVar('PromiseArg', Callable, 'Thenable')


class Thenable(collections.Callable):  # pragma: no cover

    @abc.abstractmethod
    def __call__(self, *args, **kwargs) -> Any:
        ...

    @abc.abstractmethod
    def then(self, on_success: 'PromiseArg',
             on_error: 'PromiseArg' = None) -> 'Thenable':
        ...

    @abc.abstractmethod
    def throw(self, exc: BaseException = None,
              tb: TracebackType = None,
              propagate: int = True) -> None:
        ...

    @abc.abstractmethod
    def throw1(self, exc: BaseException = None) -> None:
        ...

    @abc.abstractmethod
    def cancel(self) -> None:
        ...

    @property
    @abc.abstractmethod
    def cancelled(self) -> bool:
        ...

    @property
    @abc.abstractmethod
    def ready(self) -> bool:
        ...

    @property
    @abc.abstractmethod
    def failed(self) -> bool:
        ...

    @classmethod
    def __subclasshook__(cls: Any, C: Any) -> bool:
        if cls is Thenable:
            if any('then' in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented


@Thenable.register
class ThenableProxy:

    def _set_promise_target(self, p: Thenable) -> None:
        self._p = p

    def then(self, on_success: PromiseArg,
             on_error: PromiseArg = None) -> Thenable:
        return self._p.then(on_success, on_error)

    def cancel(self) -> None:
        self._p.cancel()

    def throw1(self, exc: BaseException = None) -> None:
        self._p.throw1(exc)

    def throw(self, exc: BaseException = None,
              tb: TracebackType = None,
              propagate: int = True) -> None:
        self._p.throw(exc, tb=tb, propagate=propagate)

    def _get_cancelled(self) -> bool:
        return self._p.cancelled

    def _set_cancelled(self, cancelled: bool) -> None:
        self._p.cancelled = cancelled
    cancelled = property(_get_cancelled, _set_cancelled)

    def _get_ready(self) -> bool:
        return self._p.ready

    def _set_ready(self, ready: bool) -> None:
        self._p.ready = ready
    ready = property(_get_ready, _set_ready)

    def _get_failed(self) -> bool:
        return self._p.failed

    def _set_failed(self, failed: bool) -> None:
        self._p.failed = failed
    failed = property(_get_failed, _set_failed)
