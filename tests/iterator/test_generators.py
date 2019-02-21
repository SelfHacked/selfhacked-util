import pytest

from selfhacked.iterator.generators import partial, report, log


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
        yield from ()

    assert gen() == ()

    @partial(empty_error=True)
    def gen2():
        yield from ()

    with pytest.raises(StopIteration):
        gen2()

    @partial(empty_error=ValueError)
    def gen3():
        yield from ()

    with pytest.raises(ValueError):
        gen3()


def test_report():
    logs = []

    @report(interval=2, interval_callback=logs.append, finish_callback=logs.append)
    def gen():
        yield from range(10)

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
        yield from range(3)

    assert list(gen()) == [0, 1, 2]
    assert logs == [
        'gen: yielded 2 entries',
        'gen: finished with 3 entries',
    ]
