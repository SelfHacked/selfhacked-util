from functools import wraps
from typing import Union, Type, Callable


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
                for item in iterator:
                    yield item

            return __new_generator()

        return __new_func

    return __decor


def report(
        interval=1000,
        interval_callback: Callable[[int], None] = None,
        finish_callback: Callable[[int], None] = None,
):
    """
    Report progress of a generator
    """

    def __decor(gen):
        @wraps(gen)
        def __new_func(*args, **kwargs):
            count = 0
            for item in gen(*args, **kwargs):
                count += 1
                if count % interval == 0:
                    if interval_callback is not None:
                        interval_callback(count)
                yield item

            if finish_callback is not None:
                finish_callback(count)

        return __new_func

    return __decor


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

        def interval_callback(n):
            log(f"{_name}: yielded {n} entries")

        def finish_callback(n):
            log(f"{_name}: finished with {n} entries")

        return report(
            interval=interval,
            interval_callback=interval_callback,
            finish_callback=finish_callback,
        )(gen)

    return __decor
