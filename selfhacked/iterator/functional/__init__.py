from typing import Iterable


def apply(func, *args, **kwargs):
    def __func(iterable: Iterable):
        for item in iterable:
            yield func(item, *args, **kwargs)

    return __func


def remove_empty(iterable: Iterable):
    for item in iterable:
        if not item:
            continue
        yield item


def yield_from(iterable: Iterable[Iterable]):
    for item in iterable:
        yield from item
