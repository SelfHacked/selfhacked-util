from typing import Iterable, Iterator

from .typing import _BaseParamFunction, T_co


class _BaseFilter(_BaseParamFunction[T_co, T_co]):
    def _match(self, item) -> bool:
        raise NotImplementedError  # pragma: no cover

    def __call__(self, iterable: Iterable[T_co]) -> Iterator[T_co]:
        for item in iterable:
            if not self._match(item):
                continue
            yield item

    def __invert__(self):
        return filter_(lambda item: not self._match(item))

    def __and__(self, other: '_BaseFilter'):
        return filter_(lambda item: self._match(item) and other._match(item))

    def __or__(self, other: '_BaseFilter'):
        return filter_(lambda item: self._match(item) or other._match(item))


class filter_(_BaseFilter[T_co]):
    """
    Check all items in the iterable, and yield only matches.
    """

    def __init__(self, match, *args, **kwargs):
        self.__match = match
        self.__args = args
        self.__kwargs = kwargs

    def _match(self, item) -> bool:
        return self.__match(item, *self.__args, **self.__kwargs)


remove_empty = filter_(bool)
