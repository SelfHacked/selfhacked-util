from typing import Iterable, Iterator

from . import apply, filter_not

strip = apply(str.strip)

remove_comments = filter_not(str.startswith, '#')


def split_lines(iterable: Iterable[str]) -> Iterator[str]:
    """
    :param iterable: a series of strings, not necessarily split by lines
    :return: a series of strings split by lines

    E.g.
        ('123', '45\n6\n') | split_lines -> ('12345\n', '6\n')
    """
    remaining = ''
    for item in iterable:
        lines = (remaining + item).splitlines(keepends=True)
        remaining = lines.pop(-1)
        yield from lines
    if remaining:
        yield remaining
