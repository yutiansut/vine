import io

# Python 3.6 sets wrapper.__wrapped__ now, so no longer
# necessary to import wraps from this module.
from functools import update_wrapper, wraps  # noqa
from typing import AnyStr, Callable, cast

__all__ = ['AnyStringIO', 'update_wrapper', 'wraps']


def want_str(s: AnyStr) -> str:
    return cast(bytes, s).decode() if isinstance(s, bytes) else cast(str, s)


class AnyStringIO(io.StringIO):

    def __init__(self, s: AnyStr = None,
                 *a, _init: Callable = io.StringIO.__init__, **kw) -> None:
        _init(self, want_str(s), *a, **kw)

    def write(self, s: AnyStr,
              _write: Callable = io.StringIO.write) -> int:
        return _write(self, want_str(s))
