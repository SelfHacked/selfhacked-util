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
