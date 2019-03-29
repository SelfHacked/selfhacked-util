from typing import Iterator, Iterable

from selfhacked.iterator.typing import T_co


class Stream(Iterator[T_co]):
    def __next__(self) -> T_co:
        raise NotImplementedError  # pragma: no cover

    def __or__(self, other) -> 'Stream':
        """
        Override the `|` operator.
        :param other: An iterator function, see `functional` package.
        """
        return IterStream(other(self))

    def __gt__(self, other):
        """
        Override the `>` operator.
        Call `other(self)`.
        """
        return other(self)

    def __call__(self) -> None:
        """
        Go through the stream with a for loop without returning anything.
        """
        for item in self:
            pass


class BaseIterStream(Stream[T_co]):
    def __init__(self):
        self.__iter: Iterator[T_co] = None

    def _iterable(self) -> Iterable[T_co]:
        raise NotImplementedError  # pragma: no cover

    def __next__(self) -> T_co:
        if self.__iter is None:
            self.__iter = iter(self._iterable())
        return next(self.__iter)


class IterStream(BaseIterStream[T_co]):
    def __init__(self, iterable: Iterable):
        super().__init__()
        self.__iterable = iterable

    def _iterable(self) -> Iterable[T_co]:
        return self.__iterable
