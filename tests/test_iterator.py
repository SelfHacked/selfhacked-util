import pytest

from selfhacked.iterator import PeekableIterator


def test_peekable():
    pi = PeekableIterator('ab')

    assert pi.peek() == 'a'
    assert next(pi) == 'a'

    assert pi.peek() == 'b'
    assert pi.peek() == 'b'
    assert next(pi) == 'b'

    with pytest.raises(StopIteration):
        pi.peek()
    with pytest.raises(StopIteration):
        pi.peek()
    with pytest.raises(StopIteration):
        next(pi)
    with pytest.raises(StopIteration):
        pi.peek()
