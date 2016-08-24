from __future__ import absolute_import, unicode_literals

import pytest


@pytest.fixture(autouse=True)
def zzzz_test_cases_calls_setup_teardown(request):
    if request.instance:
        # we set the .patching attribute for every test class.
        setup = getattr(request.instance, 'setup', None)
        # we also call .setup() and .teardown() after every test method.
        teardown = getattr(request.instance, 'teardown', None)
        setup and setup()
        teardown and request.addfinalizer(teardown)


@pytest.fixture(autouse=True)
def test_cases_has_patching(request, patching):
    if request.instance:
        request.instance.patching = patching
