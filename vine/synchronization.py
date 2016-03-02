from __future__ import absolute_import, unicode_literals

from .abstract import Thenable
from .promises import promise

__all__ = ['barrier']


class barrier(object):
    """Synchronization primitive to call a callback after a list
    of promises have been fulfilled.

    Example:

    .. code-block:: python

        # Request supports the .then() method.
        p1 = http.Request('http://a')
        p2 = http.Request('http://b')
        p3 = http.Request('http://c')
        requests = [p1, p2, p3]

        def all_done():
            pass  # all requests complete

        b = barrier(requests).then(all_done)

        # oops, we forgot we want another request
        b.add(http.Request('http://d'))

    Note that you cannot add new promises to a barrier after
    the barrier is fulfilled.

    """
    def __init__(self, promises=None, args=None, kwargs=None,
                 callback=None, size=None):
        self.p = promise()
        self.promises = []
        self.args = args or ()
        self.kwargs = kwargs or {}
        self._value = 0
        self.size = size or len(self.promises)
        self.ready = self.failed = False
        self.value = self.reason = None
        self.cancelled = False
        self.finalized = bool(promises or self.size)
        [self.add(p) for p in promises or []]
        if callback:
            self.then(callback)

    def __call__(self, *args, **kwargs):
        if not self.ready and not self.cancelled:
            self._value += 1
            if self.finalized and self._value >= self.size:
                self.ready = True
                self.p(*self.args, **self.kwargs)

    def finalize(self):
        if not self.finalized and self._value >= self.size:
            self.p(*self.args, **self.kwargs)
        self.finalized = True

    def cancel(self):
        self.cancelled = True
        self.p.cancel()

    def add_noincr(self, p):
        if not self.cancelled:
            if self.ready:
                raise ValueError('Cannot add promise to full barrier')
            p.then(self)
            self.promises.append(p)

    def add(self, p):
        if not self.cancelled:
            self.add_noincr(p)
            self.size += 1

    def then(self, callback, errback=None):
        self.p.then(callback, errback)

    def throw(self, *args, **kwargs):
        if not self.cancelled:
            self.p.throw(*args, **kwargs)
    throw1 = throw
Thenable.register(barrier)
