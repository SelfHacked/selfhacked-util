from typing import Callable, Iterable, Iterator, T_co

from . import Function


class _BaseReport(Function[T_co, T_co]):
    def __init__(self, *, interval=1000):
        self.__interval = interval

    def _interval_callback(self, n: int):
        raise NotImplementedError

    def _finish_callback(self, n: int):
        raise NotImplementedError

    def __call__(self, iterable: Iterable[T_co]) -> Iterator[T_co]:
        count = 0
        for item in iterable:
            count += 1
            if count % self.__interval == 0:
                self._interval_callback(count)
            yield item

        self._finish_callback(count)


class report(_BaseReport[T_co]):
    """
    Report progress of an iterable
    """

    @staticmethod
    def none(n: int):
        pass

    def __init__(
            self,
            *,
            interval=1000,
            interval_callback: Callable[[int], None] = None,
            finish_callback: Callable[[int], None] = None,
    ):
        super().__init__(interval=interval)
        self.__interval_callback = interval_callback or self.none
        self.__finish_callback = finish_callback or self.none

    def _interval_callback(self, n: int):
        self.__interval_callback(n)

    def _finish_callback(self, n: int):
        self.__finish_callback(n)


class log(_BaseReport[T_co]):
    """
    Log progress of an iterable
    """

    def __init__(
            self,
            *,
            log: Callable[[str], None] = print,
            name,
            interval=1000,
    ):
        super().__init__(interval=interval)
        self.__name = name
        self.__log = log

    def _interval_callback(self, n: int):
        self.__log(f"{self.__name}: yielded {n} entries")

    def _finish_callback(self, n: int):
        self.__log(f"{self.__name}: finished with {n} entries")
