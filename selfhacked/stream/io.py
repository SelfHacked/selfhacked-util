from . import Stream


class InputStream(Stream):
    def _iter(self):
        try:
            while True:
                yield input()
        except EOFError:
            return


class FileStream(Stream):
    def __init__(self, name):
        self.__name = name
        self.__f = None

    def _open(self):
        self.__f = open(self.__name)

    def _close(self):
        self.__f.close()

    def _iter(self):
        yield from self.__f
