import pytest

from selfhacked.csv.field import FieldOptions


def test_dict():
    options = FieldOptions()

    assert 'opt' not in options
    with pytest.raises(KeyError):
        opt = options['opt']

    options['opt'] = 0
    assert 'opt' in options
    assert options['opt'] == 0


def test_no_duplicate():
    options = FieldOptions()
    options['opt'] = 0
    with pytest.raises(KeyError):
        options['opt'] = 1


def test_tmp():
    options = FieldOptions()
    options['opt'] = 0
    with options.tmp(opt=1, other=2):
        assert 'opt' in options
        assert options['opt'] == 1
        assert 'other' in options
        assert options['other'] == 2
    assert 'opt' in options
    assert options['opt'] == 0
    assert 'other' not in options
