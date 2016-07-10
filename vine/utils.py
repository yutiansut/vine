import io

from functools import (
    WRAPPER_ASSIGNMENTS, WRAPPER_UPDATES,
    update_wrapper as _update_wrapper,
    partial,
)

__all__ = ['AnyStringIO', 'update_wrapper', 'wraps']


class AnyStringIO(io.StringIO):

    def __init__(self, v=None, *a, _init=io.StringIO.__init__, **kw):
        _init(self, v.decode() if isinstance(v, bytes) else v, *a, **kw)

    def write(self, data, _write=io.StringIO.write):
        _write(self, data.decode() if isinstance(data, bytes) else data)



def update_wrapper(wrapper, wrapped, *args, **kwargs):
    wrapper = _update_wrapper(wrapper, wrapped, *args, **kwargs)
    wrapper.__wrapped__ = wrapped
    return wrapper


def wraps(wrapped,
          assigned=WRAPPER_ASSIGNMENTS,
          updated=WRAPPER_UPDATES):
    return partial(update_wrapper, wrapped=wrapped,
                   assigned=assigned, updated=updated)
