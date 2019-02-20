from selfhacked.util.formatting import format_price


def test_format_price():
    assert format_price(1) == '1'
    assert format_price(1.0) == '1'

    assert format_price(1.1) == '1.10'
    assert format_price(1.11) == '1.11'
    assert format_price(1.111) == '1.11'
