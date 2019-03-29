from typing import Union

from . import Stream, BaseIterStream


class InputStream(Stream[str]):
    def __next__(self) -> str:
        try:
            return input()
        except EOFError:
            raise StopIteration


class FileStream(BaseIterStream[Union[str, bytes]]):
    def __init__(self, name, *, binary=False):
        super().__init__()
        self.__name = name
        self.__binary = binary

    @property
    def __mode(self):
        return 'rb' if self.__binary else 'r'

    def _iterable(self):
        with open(self.__name, self.__mode) as f:
            yield from f
