from typing import Iterable, Iterator, Callable, T_co, V_co

Function = Callable[[Iterable[T_co]], Iterator[V_co]]


class apply(Function[T_co, V_co]):
    """
    Apply `func` to all items in the iterable.
    `func` must take each item as the first argument, and then take *args, **kwargs
    """

    def __init__(self, func, *args, **kwargs):
        self.__func = func
        self.__args = args
        self.__kwargs = kwargs

    def __call_func(self, item):
        return self.__func(item, *self.__args, **self.__kwargs)

    def __call__(self, iterable: Iterable[T_co]) -> Iterator[V_co]:
        for item in iterable:
            yield self.__call_func(item)


class filter(Function[T_co, T_co]):
    """
    Check all items in the iterable, and yield only matches.
    """

    def __init__(self, match, *args, **kwargs):
        self.__match = match
        self.__args = args
        self.__kwargs = kwargs

    def __call_match(self, item):
        return self.__match(item, *self.__args, **self.__kwargs)

    def __call__(self, iterable: Iterable[T_co]) -> Iterator[T_co]:
        for item in iterable:
            if not self.__call_match(item):
                continue
            yield item

    def __invert__(self):
        return filter(lambda item: not self.__call_match(item))

    def __and__(self, other: 'filter'):
        return filter(lambda item: self.__call_match(item) and other.__call_match(item))

    def __or__(self, other: 'filter'):
        return filter(lambda item: self.__call_match(item) or other.__call_match(item))


remove_empty = filter(bool)


def yield_from(iterable: Iterable[Iterable]) -> Iterator:
    """
    Unpack a series of iterables into one iterable.
    """
    for item in iterable:
        yield from item
