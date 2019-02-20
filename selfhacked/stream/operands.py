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


decode = apply(bytes.decode, encoding='utf-8')


def split_lines(iterable: Iterable[str]):
    remaining = ''
    for item in iterable:
        lines = (remaining + item).splitlines(keepends=True)
        remaining = lines.pop(-1)
        yield from lines
    if remaining:
        yield remaining
