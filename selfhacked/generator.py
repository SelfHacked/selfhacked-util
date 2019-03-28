from functools import wraps
from typing import Union, Type, Callable

from selfhacked.iterator.functional import (
    Function,
    filter as _filter,
    remove_empty as _remove_empty,
)
from selfhacked.iterator.functional.counting import (
    report as _report,
    log as _log,
)


class partial(object):
    """
    Decorates a generator so that when called,
    it's partially executed until the first `yield` statement.
    If the result is empty (i.e. a `yield` statement is never reached),
    0. The generator will be fully executed; and
    1. If `empty_error` is False (default), an empty generator will be returned; otherwise
    2. If `empty_error` is True, a StopIteration will be raised; otherwise
    3. `empty_error()` will be raised
    """

    def __init__(
            self,
            *,
            empty_error: Union[bool, Type[Exception]] = False
    ):
        self.__empty_error = empty_error

    def __call__(self, gen):
        @wraps(gen)
        def __new_func(*args, **kwargs):
            iterator = gen(*args, **kwargs)
            try:
                first = next(iterator)
            except StopIteration:
                if not self.__empty_error:
                    return iter(())
                elif self.__empty_error is True:
                    raise
                else:
                    raise self.__empty_error() from None

            def __new_generator():
                yield first
                yield from iterator

            return __new_generator()

        return __new_func


class functional(object):
    """
    Change a iterator function (see `iterator.functional`) to a generator decorator
    """

    def __init__(self, func: Function, *, has_params: bool):
        self.__doc__ = func.__doc__
        self.__has_params = has_params

        class __new_func(object):
            def __init__(self, *args, **kwargs):
                if has_params:
                    self.__f = func(*args, **kwargs)
                else:
                    self.__f = func

            def __call__(self, gen):
                @wraps(gen)
                def __new_gen(*args, **kwargs):
                    return self.__f(gen(*args, **kwargs))

                return __new_gen

        self.__new_func = __new_func

    def __call__(self, *args, **kwargs):
        if self.__has_params:
            return self.__new_func(*args, **kwargs)
        else:
            return self.__new_func()(args[0])


filter = functional(_filter, has_params=True)

remove_empty = functional(_remove_empty, has_params=False)

report = functional(_report, has_params=True)


class log(object):
    __self = functional(_log, has_params=True)

    """
    Log progress of a generator
    """

    def __init__(
            self,
            *,
            log: Callable[[str], None] = print,
            name=None,
            interval=1000,
    ):
        self.__log = log
        self.__name = name
        self.__interval = interval

    def __call__(self, gen):
        name = self.__name or gen.__name__
        return self.__self(
            log=self.__log,
            name=name,
            interval=self.__interval,
        )(gen)
