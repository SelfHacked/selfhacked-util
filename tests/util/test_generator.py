import pytest

from selfhacked.util.generator import partial, report, log


def test_partial():
    @partial()
    def gen(out_list):
        out_list.append(0)
        yield 1
        out_list.append(2)

    results = []
    generator = gen(results)
    assert results == [0]
    assert list(generator) == [1]
    assert results == [0, 2]


def test_empty():
    @partial()
    def gen():
        for i in ():
            yield i

    assert gen() == ()

    @partial(empty_error=True)
    def gen2():
        for i in ():
            yield i

    with pytest.raises(StopIteration):
        gen2()

    @partial(empty_error=ValueError)
    def gen3():
        for i in ():
            yield i

    with pytest.raises(ValueError):
        gen3()


def test_report():
    logs = []

    @report(interval=2, interval_callback=logs.append, finish_callback=logs.append)
    def gen():
        for i in range(10):
            yield i

    generator = gen()
    assert next(generator) == 0
    assert logs == []

    assert next(generator) == 1
    assert logs == [2]

    assert list(generator) == [2, 3, 4, 5, 6, 7, 8, 9]
    assert logs == [2, 4, 6, 8, 10, 10]


def test_log():
    logs = []

    @log(log=logs.append, interval=2)
    def gen():
        for i in range(3):
            yield i

    assert list(gen()) == [0, 1, 2]
    assert logs == [
        'gen: yielded 2 entries',
        'gen: finished with 3 entries',
    ]
