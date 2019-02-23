from selfhacked.iterator.functional import remove_empty, yield_from


def test_remove_empty():
    assert tuple(remove_empty(('123', '', 'abc'))) == ('123', 'abc')


def test_yield_from():
    assert tuple(yield_from(('123', '456'))) == tuple('123456')
