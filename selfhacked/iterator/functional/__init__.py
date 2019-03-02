from typing import Iterable, Iterator


def apply(func, *args, **kwargs):
    """
    Apply `func` to all items in the iterable.
    `func` must take each item as the first argument, and then take *args, **kwargs
    """

    def __func(iterable: Iterable) -> Iterator:
        for item in iterable:
            yield func(item, *args, **kwargs)

    return __func


def filter(match, *args, **kwargs):
    """
    Check all items in the iterable, and yield only matches.
    """

    def __func(iterable: Iterable) -> Iterator:
        for item in iterable:
            if not match(item, *args, **kwargs):
                continue
            yield item

    return __func


def filter_not(match, *args, **kwargs):
    """
    Check all items in the iterable, and yield only non-matches.
    """

    def __func(iterable: Iterable) -> Iterator:
        for item in iterable:
            if match(item, *args, **kwargs):
                continue
            yield item

    return __func


remove_empty = filter(bool)


def yield_from(iterable: Iterable[Iterable]) -> Iterator:
    """
    Unpack a series of iterables into one iterable.
    """
    for item in iterable:
        yield from item
