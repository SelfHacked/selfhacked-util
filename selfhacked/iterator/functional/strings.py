from typing import Iterable

from . import apply

strip = apply(str.strip)


def remove_comments(iterable: Iterable[str]):
    for item in iterable:
        if item.startswith('#'):
            continue
        yield item


def split_lines(iterable: Iterable[str]):
    remaining = ''
    for item in iterable:
        lines = (remaining + item).splitlines(keepends=True)
        remaining = lines.pop(-1)
        yield from lines
    if remaining:
        yield remaining
