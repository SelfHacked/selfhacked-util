from selfhacked.util.func import returns


def test_returns():
    @returns(list)
    def f(n):
        for i in range(n):
            yield i ** 2

    result = f(5)
    assert isinstance(result, list)
    assert result == [i ** 2 for i in range(5)]
