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
    ri = ReadableIterator('abc', empty='')

    assert ri.readline() == 'a'
    assert ri.readlines() == ['b', 'c']
    assert ri.readline() == ''


@pytest.mark.depenedency(
    depends=['test_readable'],
)
def test_readable_read():
    ri = ReadableIterator(['abc', 'd', 'ef'], empty='')

    assert ri.read(1) == 'a'
    assert ri.readline() == 'bc'
    assert ri.read() == 'def'
    assert ri.read() == ''
