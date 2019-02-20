import pytest

from selfhacked.iterator import PeekIterator, ReadableIterator


def test_peek():
    pi = PeekIterator('ab')

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
    depends=['test_peek'],
)
def test_readable():
    ri = ReadableIterator('abc')

    assert ri.readable()
    assert ri.readline() == 'a'
    assert ri.readlines() == ['b', 'c']
    with pytest.raises(EOFError):
        assert ri.readline()
    assert not ri.readable()


@pytest.mark.depenedency(
    depends=['test_readable'],
)
def test_readable_read():
    ri = ReadableIterator(['abc', 'd', 'ef'])

    assert ri.readable()
    assert ri.read(1) == 'a'
    assert ri.readline() == 'bc'
    assert ri.read() == 'def'
    with pytest.raises(EOFError):
        assert ri.read()
    assert not ri.readable()
