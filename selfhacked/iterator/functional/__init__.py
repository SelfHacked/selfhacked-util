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


def remove_empty(iterable: Iterable) -> Iterator:
    """
    Remove items that are evaluated as False.
    """
    for item in iterable:
        if not item:
            continue
        yield item


def yield_from(iterable: Iterable[Iterable]) -> Iterator:
    """
    Unpack a series of iterables into one iterable.
    """
    for item in iterable:
        yield from item
