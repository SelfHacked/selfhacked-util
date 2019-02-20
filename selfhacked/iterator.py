from typing import Iterator


class PeekIterator(Iterator):
    def __init__(self, iterator: Iterator):
        self.__iter = iter(iterator)

        self._empty = False
        self._next = None
        self._forward()

    def _forward(self):
        try:
            self._next = next(self.__iter)
        except StopIteration:
            self._empty = True

    def peek(self):
        if self._empty:
            raise StopIteration
        return self._next

    def __next__(self):
        result = self.peek()
        self._forward()
        return result


class ReadableIterator(PeekIterator):
    def __init__(self, iterator: Iterator, empty):
        super().__init__(iterator)
        self.empty = empty

    def readline(self):
        try:
            return next(self)
        except StopIteration:
            return self.empty

    def read(self, size: int = None):
        try:
            result = self.empty
        except StopIteration:
            return self.empty
        while True:
            try:
                result += self.peek()
            except StopIteration:
                return result
            if size is not None and len(result) > size:
                self._next = result[size:]
                result = result[:size]
                return result
            else:
                self._forward()

    def readlines(self):
        return list(self)
