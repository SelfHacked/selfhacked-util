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
    def __init__(self, iterator: Iterator):
        super().__init__(iterator)

    @property
    def empty(self):
        try:
            return self.peek()[0:0]
        except StopIteration:
            raise EOFError from None

    def readable(self):
        try:
            self.peek()
        except StopIteration:
            return False
        else:
            return True

    def readline(self):
        try:
            return next(self)
        except StopIteration:
            raise EOFError from None

    def read(self, size: int = None):
        result = self.empty
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
