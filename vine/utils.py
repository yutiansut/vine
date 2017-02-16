"""Python compatiblity utilities."""
# Python 3.6 sets wrapper.__wrapped__ now, so no longer
# necessary to import wraps from this module.
from functools import (  # noqa
    WRAPPER_ASSIGNMENTS, WRAPPER_UPDATES,
    update_wrapper, wraps,
)

__all__ = ['update_wrapper', 'wraps']


def update_wrapper(wrapper, wrapped, *args, **kwargs):
    """Update wrapper, also setting .__wrapped__."""
    wrapper = _update_wrapper(wrapper, wrapped, *args, **kwargs)
    wrapper.__wrapped__ = wrapped
    return wrapper


def wraps(wrapped,
          assigned=WRAPPER_ASSIGNMENTS,
          updated=WRAPPER_UPDATES):
    """Backport of Python 3.5 wraps that adds .__wrapped__."""
    return partial(update_wrapper, wrapped=wrapped,
                   assigned=assigned, updated=updated)
