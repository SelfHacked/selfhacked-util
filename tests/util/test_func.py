from selfhacked.util.func import returns, timed, log_time


def test_returns():
    @returns(list)
    def f(n):
        for i in range(n):
            yield i ** 2

    result = f(5)
    assert isinstance(result, list)
    assert result == [i ** 2 for i in range(5)]


def test_timed():
    logs = []

    @timed(logs.append)
    def long():
        for i in range(10000):
            pass

    long()
    assert len(logs) == 1
    assert isinstance(logs[0], float)


def test_log_time():
    logs = []

    @log_time(logs.append)
    def long():
        for i in range(10):
            pass

    long()
    assert len(logs) == 1
    out = logs[0].split()
    assert len(out) == 5
    assert out[:3] == ['long', 'call', 'took']
    float(out[3])  # no exception should be raised here
    assert out[-1] == 'seconds'
