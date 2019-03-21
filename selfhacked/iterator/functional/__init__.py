from typing import Iterable, Iterator, Callable, T_co, V_co

Function = Callable[[Iterable[T_co]], Iterator[V_co]]


class _BaseOneToOneFunction(Function[T_co, V_co]):
    def _call(self, item):
        raise NotImplementedError  # pragma: no cover

    def __call__(self, iterable: Iterable[T_co]) -> Iterator[V_co]:
        for item in iterable:
            yield self._call(item)


class apply(_BaseOneToOneFunction[T_co, V_co]):
    """
    Apply `func` to all items in the iterable.
    `func` must take each item as the first argument, and then take *args, **kwargs
    """

    def __init__(self, func, *args, **kwargs):
        self.__func = func
        self.__args = args
        self.__kwargs = kwargs

    def _call(self, item):
        return self.__func(item, *self.__args, **self.__kwargs)


class _BaseFilter(Function[T_co, T_co]):
    def _match(self, item) -> bool:
        raise NotImplementedError  # pragma: no cover

    def __call__(self, iterable: Iterable[T_co]) -> Iterator[T_co]:
        for item in iterable:
            if not self._match(item):
                continue
            yield item

    def __invert__(self):
        return filter(lambda item: not self._match(item))

    def __and__(self, other: '_BaseFilter'):
        return filter(lambda item: self._match(item) and other._match(item))

    def __or__(self, other: '_BaseFilter'):
        return filter(lambda item: self._match(item) or other._match(item))


class filter(_BaseFilter[T_co]):
    """
    Check all items in the iterable, and yield only matches.
    """

    def __init__(self, match, *args, **kwargs):
        self.__match = match
        self.__args = args
        self.__kwargs = kwargs

    def _match(self, item) -> bool:
        return self.__match(item, *self.__args, **self.__kwargs)


remove_empty = filter(bool)


def yield_from(iterable: Iterable[Iterable]) -> Iterator:
    """
    Unpack a series of iterables into one iterable.
    """
    for item in iterable:
        yield from item
