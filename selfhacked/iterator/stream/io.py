from . import Stream


class InputStream(Stream):
    def _iter(self):
        try:
            while True:
                yield input()
        except EOFError:
            return


class FileStream(Stream):
    def __init__(self, name, *, binary=False):
        self.__name = name
        self.__binary = binary
        self.__f = None

    @property
    def __mode(self):
        return 'rb' if self.__binary else 'r'

    def _open(self):
        self.__f = open(self.__name, self.__mode)

    def _close(self):
        self.__f.close()

    def _iter(self):
        yield from self.__f
