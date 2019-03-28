from contextlib import contextmanager
from time import time


@contextmanager
def assert_time(
        expected_time,
        *,
        margin=0.02,
):
    start = time()
    try:
        yield
    finally:
        t = time() - start
        print(t)
        assert -margin <= t - expected_time <= margin
