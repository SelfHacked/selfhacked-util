from typing import Callable, Iterable, Iterator


def report(
        *,
        interval=1000,
        interval_callback: Callable[[int], None] = None,
        finish_callback: Callable[[int], None] = None,
):
    """
    Report progress of a iterable
    """

    def __func(iterable: Iterable) -> Iterator:
        count = 0
        for item in iterable:
            count += 1
            if count % interval == 0:
                if interval_callback is not None:
                    interval_callback(count)
            yield item

        if finish_callback is not None:
            finish_callback(count)

    return __func


def log(
        name,
        *,
        log: Callable[[str], None] = print,
        interval=1000,
):
    """
    Log progress of a iterable
    """

    def __func(iterable: Iterable) -> Iterator:
        def interval_callback(n):
            log(f"{name}: yielded {n} entries")

        def finish_callback(n):
            log(f"{name}: finished with {n} entries")

        return report(
            interval=interval,
            interval_callback=interval_callback,
            finish_callback=finish_callback,
        )(iterable)

    return __func
