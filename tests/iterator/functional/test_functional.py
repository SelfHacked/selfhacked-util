from selfhacked.iterator.functional import remove_empty


def test_remove_empty():
    assert tuple(remove_empty(('123', '', 'abc'))) == ('123', 'abc')
