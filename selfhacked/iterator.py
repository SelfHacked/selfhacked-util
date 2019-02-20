from typing import Iterator


class PeekableIterator(Iterator):
    def __init__(self, iterator: Iterator):
        self.__iter = iter(iterator)

        self.__next = None
        self.__peeked = False

    def peek(self):
        self.__next = next(self)
        self.__peeked = True
        return self.__next

    def __next__(self):
        if self.__peeked:
            self.__peeked = False
            return self.__next
        return next(self.__iter)


class ReadableIterator(PeekableIterator):
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
