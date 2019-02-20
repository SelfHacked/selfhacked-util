from typing import Iterator, Iterable


class Stream(Iterable):
    def _open(self):
        pass

    def _close(self):
        pass

    def _iter(self) -> Iterator:
        raise NotImplementedError

    def __iter__(self):
        self._open()
        try:
            yield from self._iter()
        finally:
            self._close()

    def __or__(self, other):
        return IterStream(other(self))


class IterStream(Stream):
    def __init__(self, iterable: Iterable):
        self.__iter = iterable

    def _iter(self):
        yield from self.__iter
