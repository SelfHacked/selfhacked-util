import time

from functools import wraps
from typing import Callable


def returns(type):
    def __decor(func):
        @wraps(func)
        def __new_func(*args, **kwargs):
            return type(func(*args, **kwargs))

        return __new_func

    return __decor


def timed(
        callback: Callable[[float], None]
):
    def __decor(func):
        @wraps(func)
        def __new_func(*args, **kwargs):

            start = time.time()
            try:
                return func(*args, **kwargs)
            finally:
                callback(time.time() - start)

        return __new_func

    return __decor


def log_time(
        log: Callable[[str], None] = print,
        name=None,
):
    def __decor(func):
        _name = name or func.__name__

        def callback(t):
            log(f"{_name} call took {t} seconds")

        return timed(callback=callback)(func)

    return __decor
