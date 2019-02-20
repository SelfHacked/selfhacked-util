from time import sleep

import pytest

from selfhacked.iterator.threading import ThreadedPrefetchOneIterator, ThreadedPrefetchAllIterator
from selfhacked.testing import assert_time


def dummy_iterable():
    sleep(0.1)
    yield 0
    sleep(0.1)
    yield 1


def _test_prefetch(cls):
    iterator = cls(dummy_iterable())

    with assert_time(0.1):
        assert next(iterator) == 0

    sleep(0.1)
    # the second record should have been prefetched by now
    with assert_time(0):
        assert next(iterator) == 1

    with pytest.raises(StopIteration):
        next(iterator)


def test_prefetch_one():
    _test_prefetch(ThreadedPrefetchOneIterator)


def test_prefetch_all():
    _test_prefetch(ThreadedPrefetchAllIterator)


def test_timeout():
    iterator = ThreadedPrefetchAllIterator(dummy_iterable(), timeout=0)
    with pytest.raises(iterator.Timeout):
        next(iterator)


def test_wait():
    iterator = ThreadedPrefetchAllIterator(dummy_iterable(), sleep=0.3)
    with assert_time(0.3):
        assert next(iterator) == 0

    # the second record should have been prefetched by now
    with assert_time(0):
        assert next(iterator) == 1
