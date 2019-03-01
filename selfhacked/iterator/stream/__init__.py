from typing import Iterator, Iterable, T_co


class Stream(Iterable[T_co]):
    def _open(self):
        pass

    def _close(self):
        pass

    def _iter(self) -> Iterator[T_co]:
        raise NotImplementedError

    def __iter__(self):
        self._open()
        try:
            yield from self._iter()
        finally:
            self._close()

    def __or__(self, other) -> 'Stream':
        """
        Override the `|` operator.
        :param other: An iterator function, see `functional` package.
        """
        return IterStream(other(self))


class IterStream(Stream[T_co]):
    def __init__(self, iterable: Iterable):
        self.__iter = iterable

    def _iter(self):
        yield from self.__iter
