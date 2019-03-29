from typing import Iterable, Iterator

from .typing import _BaseParamFunction, T_co, V_co


class _BaseOneToOneFunction(_BaseParamFunction[T_co, V_co]):
    def _call(self, item):
        raise NotImplementedError  # pragma: no cover

    def __call__(self, iterable: Iterable[T_co]) -> Iterator[V_co]:
        for item in iterable:
            yield self._call(item)


class apply_each(_BaseOneToOneFunction[T_co, V_co]):
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
