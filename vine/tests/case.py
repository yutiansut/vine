from __future__ import absolute_import

import importlib
import os
import sys

from contextlib import contextmanager
from functools import wraps
from io import StringIO

try:
    from unittest import mock
except ImportError:
    import mock  # noqa

from nose import SkipTest

try:
    import unittest
    unittest.skip
except AttributeError:
    import unittest2 as unittest  # noqa

PY3 = sys.version_info[0] == 3

ANY = mock.ANY
MagicMock = mock.MagicMock
patch = mock.patch
call = mock.call


class Case(unittest.TestCase):

    def setUp(self):
        self.setup()

    def tearDown(self):
        self.teardown()

    def assertItemsEqual(self, a, b, *args, **kwargs):
        return self.assertEqual(sorted(a), sorted(b), *args, **kwargs)
    assertSameElements = assertItemsEqual

    def setup(self):
        pass

    def teardown(self):
        pass

    def patch(self, *path, **options):
        manager = patch(".".join(path), **options)
        patched = manager.start()
        self.addCleanup(manager.stop)
        return patched


def PromiseMock(*args, **kwargs):
    m = Mock(*args, **kwargs)

    def on_throw(exc=None, *args, **kwargs):
        if exc:
            raise exc
        raise
    m.throw.side_effect = on_throw
    m.set_error_state.side_effect = on_throw
    m.throw1.side_effect = on_throw
    return m


def case_requires(package, *more_packages):
    packages = [package] + list(more_packages)

    def attach(cls):
        setup = cls.setUp

        @wraps(setup)
        def around_setup(self):
            for package in packages:
                try:
                    importlib.import_module(package)
                except ImportError:
                    raise SkipTest('{0} is not installed'.format(package))
            setup(self)
        cls.setUp = around_setup
        return cls
    return attach


def case_no_pypy(cls):
    setup = cls.setUp

    @wraps(setup)
    def around_setup(self):
        if getattr(sys, 'pypy_version_info', None):
            raise SkipTest('pypy incompatible')
        setup(self)
    cls.setUp = around_setup
    return cls


def case_no_python3(cls):
    setup = cls.setUp

    @wraps(setup)
    def around_setup(self):
        if PY3:
            raise SkipTest('Python 3 incompatible')
        setup(self)
    cls.setUp = around_setup
    return cls


class Mock(mock.Mock):

    def __init__(self, *args, **kwargs):
        attrs = kwargs.pop('attrs', None) or {}
        super(Mock, self).__init__(*args, **kwargs)
        for attr_name, attr_value in attrs.items():
            setattr(self, attr_name, attr_value)


class _ContextMock(Mock):
    """Dummy class implementing __enter__ and __exit__
    as the with statement requires these to be implemented
    in the class, not just the instance."""

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        pass


def ContextMock(*args, **kwargs):
    obj = _ContextMock(*args, **kwargs)
    obj.attach_mock(Mock(), '__enter__')
    obj.attach_mock(Mock(), '__exit__')
    obj.__enter__.return_value = obj
    # if __exit__ return a value the exception is ignored,
    # so it must return None here.
    obj.__exit__.return_value = None
    return obj


class MockPool(object):

    def __init__(self, value=None):
        self.value = value or ContextMock()

    def acquire(self, **kwargs):
        return self.value


def redirect_stdouts(fun):

    @wraps(fun)
    def _inner(*args, **kwargs):
        sys.stdout = StringIO()
        sys.stderr = StringIO()
        try:
            return fun(*args, **dict(kwargs,
                                     stdout=sys.stdout, stderr=sys.stderr))
        finally:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

    return _inner


def skip_if_pypy(fun):

    @wraps(fun)
    def _skips_if_pypy(*args, **kwargs):
        if getattr(sys, 'pypy_version_info', None):
            raise SkipTest('pypy incompatible')
        return fun(*args, **kwargs)

    return _skips_if_pypy


def skip_if_environ(env_var_name):

    def _wrap_test(fun):

        @wraps(fun)
        def _skips_if_environ(*args, **kwargs):
            if os.environ.get(env_var_name):
                raise SkipTest('SKIP %s: %s set\n' % (
                    fun.__name__, env_var_name))
            return fun(*args, **kwargs)

        return _skips_if_environ

    return _wrap_test


def skip_if_module(module):
    def _wrap_test(fun):
        @wraps(fun)
        def _skip_if_module(*args, **kwargs):
            try:
                __import__(module)
                raise SkipTest('SKIP %s: %s available\n' % (
                    fun.__name__, module))
            except ImportError:
                pass
            return fun(*args, **kwargs)
        return _skip_if_module
    return _wrap_test


def skip_if_not_module(module, import_errors=(ImportError,)):
    def _wrap_test(fun):
        @wraps(fun)
        def _skip_if_not_module(*args, **kwargs):
            try:
                __import__(module)
            except import_errors:
                raise SkipTest('SKIP %s: %s available\n' % (
                    fun.__name__, module))
            return fun(*args, **kwargs)
        return _skip_if_not_module
    return _wrap_test


@contextmanager
def set_module_symbol(module, key, value):
    module = importlib.import_module(module)
    prev = getattr(module, key)
    setattr(module, key, value)
    try:
        yield
    finally:
        setattr(module, key, prev)
