from functools import wraps
from typing import Union, Type, Callable

from .functional.counting import report as _report, log as _log


def partial(
        empty_error: Union[bool, Type[Exception]] = False
):
    """
    Decorates a generator so that when called,
    it's partially executed until the first `yield` statement.
    If the result is empty (i.e. a `yield` statement is never reached),
    0. The generator will be fully executed; and
    1. If `empty_error` is False (default), an empty tuple will be returned; otherwise
    2. If `empty_error` is True, a StopIteration will be raised; otherwise
    3. `empty_error()` will be raised
    """

    def __decor(gen):
        @wraps(gen)
        def __new_func(*args, **kwargs):
            iterator = gen(*args, **kwargs)
            try:
                first = next(iterator)
            except StopIteration:
                if not empty_error:
                    return ()
                elif empty_error is True:
                    raise
                else:
                    raise empty_error() from None

            def __new_generator():
                yield first
                yield from iterator

            return __new_generator()

        return __new_func

    return __decor


def functional(func, has_params):
    @wraps(func)
    def __new_func(*args, **kwargs):
        if has_params:
            f = func(*args, **kwargs)
        else:
            f = func

        def __decor(gen):
            @wraps(gen)
            def __new_gen(*args, **kwargs):
                return f(gen(*args, **kwargs))

            return __new_gen

        return __decor

    if has_params:
        return __new_func
    else:
        return __new_func()


report = functional(_report, has_params=True)


def log(
        log: Callable[[str], None] = print,
        name=None,
        interval=1000,
):
    """
    Log progress of a generator
    """

    def __decor(gen):
        _name = name or gen.__name__
        return functional(_log, has_params=True)(
            _name,
            log=log,
            interval=interval,
        )(gen)

    return __decor
