import time

from functools import wraps
from typing import Callable, Type


class returns(object):
    def __init__(self, type: Type):
        self.__type = type

    def __call__(self, func):
        @wraps(func)
        def __new_func(*args, **kwargs):
            return self.__type(func(*args, **kwargs))

        return __new_func


class _BaseTimed(object):
    def _callback(self, func, dt: float):
        raise NotImplementedError  # pragma: no cover

    def __call__(self, func):
        @wraps(func)
        def __new_func(*args, **kwargs):

            start = time.time()
            try:
                return func(*args, **kwargs)
            finally:
                self._callback(func, time.time() - start)

        return __new_func


class timed(_BaseTimed):
    def __init__(self, callback: Callable[[float], None]):
        self.__callback = callback

    def _callback(self, func, dt: float):
        self.__callback(dt)


class log_time(_BaseTimed):
    def __init__(
            self,
            *,
            log: Callable[[str], None] = print,
            name=None,
    ):
        self.__log = log
        self.__name = name

    def _callback(self, func, dt: float):
        name = self.__name or func.__name__
        self.__log(f"{name} call took {dt} seconds")
