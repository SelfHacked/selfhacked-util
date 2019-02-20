from typing import Iterator


class PeekIterator(Iterator):
    def __init__(self, iterator: Iterator):
        self.__iter = iter(iterator)

        self.__empty = False
        self.__next = None
        self.__forward()

    def __forward(self):
        try:
            self.__next = next(self.__iter)
        except StopIteration:
            self.__empty = True

    def peek(self):
        if self.__empty:
            raise StopIteration
        return self.__next

    def __next__(self):
        result = self.peek()
        self.__forward()
        return result


class ReadableIterator(PeekIterator):
    def __init__(self, iterator: Iterator):
        super().__init__(iterator)

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

    read = readline

    def readlines(self):
        return list(self)
