import pytest

from selfhacked.iterator import remove_empty, yield_from, filter


def test_filter():
    f = filter(lambda x: x % 2 == 0)
    assert tuple(f(range(10))) == tuple(range(0, 10, 2))


@pytest.mark.dependency(
    depends=['test_filter'],
)
def test_filter_logical():
    f1 = filter(lambda x: x % 2 == 0)
    f2 = filter(lambda x: x % 3 == 0)
    assert tuple((f1 | f2)(range(10))) == (0, 2, 3, 4, 6, 8, 9)
    assert tuple((f1 & f2)(range(10))) == (0, 6)


def test_remove_empty():
    assert tuple(remove_empty(('123', '', 'abc'))) == ('123', 'abc')


def test_yield_from():
    assert tuple(yield_from(('123', '456'))) == tuple('123456')
