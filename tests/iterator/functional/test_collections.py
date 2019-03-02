from selfhacked.iterator.functional.collections import getitem


def test_getitem():
    get_1 = getitem(1)
    assert tuple(get_1(('123', '45', 'abc'))) == ('2', '5', 'b')
