import pytest

from selfhacked.iterator import PeekableIterator, ReadableIterator


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


@pytest.mark.dependency(
    depends=['test_peekable'],
)
def test_readable():
    ri = ReadableIterator('abc')

    assert ri.readable()
    assert ri.readline() == 'a'
    assert ri.read() == 'b'
    assert ri.readlines() == ['c']
    with pytest.raises(EOFError):
        assert ri.readline()
    assert not ri.readable()
