from typing import TypeVar, Callable, Iterable, Iterator

T_co = TypeVar('T_co', covariant=True)  # Any type covariant containers.
V_co = TypeVar('V_co', covariant=True)  # Any type covariant containers.

Function = Callable[[Iterable[T_co]], Iterator[V_co]]


class _BaseParamFunction(Function[T_co, V_co]):
    def __call__(self, iterable: Iterable[T_co]) -> Iterator[V_co]:
        raise NotImplementedError  # pragma: no cover
