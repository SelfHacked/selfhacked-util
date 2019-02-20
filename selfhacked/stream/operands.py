from typing import Iterable


def apply(func, *args, **kwargs):
    def __op(iterable):
        for item in iterable:
            yield func(item, *args, **kwargs)

    return __op


strip = apply(str.strip)


def remove_empty(iterable):
    for item in iterable:
        if not item:
            continue
        yield item


def remove_comments(iterable: Iterable[str]):
    for item in iterable:
        if item.startswith('#'):
            continue
        yield item
