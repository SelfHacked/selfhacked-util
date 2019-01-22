from contextlib import contextmanager


class Context(object):
    class ContextError(Exception):
        pass

    class NoContext(ContextError):
        def __init__(self):
            super().__init__("Please run in a `with` context.")

    class Mismatch(ContextError):
        def __init__(self):
            super().__init__("Please run in the same `with` context.")

    __stack = []

    @classmethod
    def get_context(cls):
        if not cls.__stack:
            raise cls.NoContext
        return cls.__stack[-1]

    @classmethod
    def check_context(cls, match):
        if cls.get_context() != match:
            raise cls.Mismatch

    def __init__(self):
        self.__items = []

    def __call__(self, item):
        self.__items.append(item)

    def __iter__(self):
        yield from self.__items

    def get_items(self, type):
        for item in self:
            if isinstance(item, type):
                yield item

    @contextmanager
    def context(self):
        self.__stack.append(self)
        try:
            yield
        finally:
            self.__stack.pop(-1)

    @classmethod
    @contextmanager
    def new_context(cls):
        context = cls()
        with context.context():
            try:
                yield context
            finally:
                pass
