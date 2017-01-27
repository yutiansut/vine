import pytest
from case import Mock
from vine.promises import promise
from vine.synchronization import barrier


class test_barrier:

    def setup(self) -> None:
        self.m1, self.m2, self.m3 = Mock(), Mock(), Mock()
        self.ps = [promise(self.m1), promise(self.m2), promise(self.m3)]

    def test_evaluate(self) -> None:
        x = barrier(self.ps)
        x()
        assert not x.ready
        x()
        assert not x.ready
        x.add(promise())
        x()
        assert not x.ready
        x()
        assert x.ready
        x()
        x()

        with pytest.raises(ValueError):
            x.add(promise())

    def test_reverse(self) -> None:
        callback = Mock()
        x = barrier(self.ps, callback=promise(callback))
        for p in self.ps:
            p()
        assert x.ready
        callback.assert_called_with()

    def test_cancel(self) -> None:
        x = barrier(self.ps)
        x.cancel()
        for p in self.ps:
            p()
        x.add(promise())
        x.throw(KeyError())
        assert not x.ready

    def test_throw(self) -> None:
        x = barrier(self.ps)
        with pytest.raises(KeyError):
            x.throw(KeyError(10))
