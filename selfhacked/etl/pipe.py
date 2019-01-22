from typing import Iterator


class Pipe(Iterator):
    STATUS_SETUP = 1
    STATUS_READY = 2
    STATUS_USED = 3
    STATUS_FINISHED = 4

    class PipeStatusError(Exception):
        def __init__(self, status):
            self.status = status
            super().__init__(f"{self.__class__.__name__}: status {status}")

    class PipeNotReady(PipeStatusError):
        pass

    class PipeNotAcceptingFeed(PipeStatusError):
        pass

    class UsedPipe(Exception):
        pass

    def __init__(self, parent, key):
        self.__parent = parent
        self.__upstream_key = key
        self.__status = self.STATUS_SETUP
        self.__iterable = None

        self.__receiver = None
        self.__downstream_key = None

    @property
    def upstream(self):
        return self.__parent, self.__upstream_key

    def __or__(self, other):
        if self.__receiver is not None:
            raise self.UsedPipe
        if isinstance(other, tuple):
            receiver, key = other
        else:
            receiver = other
            key = None
        self.__receiver = receiver
        self.__downstream_key = key
        receiver.add_input(self, key)

    @property
    def downstream(self):
        return self.__receiver, self.__downstream_key

    @property
    def status(self):
        return self.__status

    def _set_status(self, status):
        self.__status = status

    @property
    def accepts_feed(self):
        return self.status == self.STATUS_SETUP

    def _set_ready(self):
        self._set_status(self.STATUS_READY)

    @property
    def _iterable(self):
        return self.__iterable

    @_iterable.setter
    def _iterable(self, iterable):
        self.__iterable = self._wrap_iterable(iterable)

    def _use(self):
        self._set_status(self.STATUS_USED)

    def _finish(self):
        self._set_status(self.STATUS_FINISHED)

    def _wrap_iterable(self, iterable):
        self._use()
        yield from iterable
        self._finish()

    def feed(self, iterable):
        if not self.accepts_feed:
            raise self.PipeNotAcceptingFeed(self.status)
        self._iterable = iterable
        self._set_ready()

    def __bool__(self):
        """
        Ready to call next()
        """
        return self.status in (self.STATUS_READY, self.STATUS_USED)

    def __next__(self):
        if self.accepts_feed:
            raise self.PipeNotReady(self.status)
        return next(self.__iterable)


class AbstractPipes(object):
    class PipeKeyError(Exception):
        def __init__(self, key):
            self.key = key
            super().__init__(f"{self.__class__.__name__}: {key}")

    class UnexpectedPipe(PipeKeyError):
        pass

    class ExistingPipe(PipeKeyError):
        pass

    def __init__(self):
        self.__pipes = {}

    def expects(self, key) -> bool:
        raise NotImplementedError

    def missing(self) -> bool:
        raise NotImplementedError

    def keys(self):
        return self.__pipes.keys()

    def __contains__(self, key):
        return key in self.__pipes

    def __len__(self):
        return len(self.__pipes)

    def __iter__(self):
        return iter(self.__pipes)

    def _add(self, key, pipe: Pipe):
        self.__pipes[key] = pipe

    def __getitem__(self, key) -> Pipe:
        try:
            return self.__pipes[key]
        except KeyError:
            raise self.PipeKeyError(key) from None

    def __setitem__(self, key, pipe: Pipe):
        if not self.expects(key):
            raise self.UnexpectedPipe(key)
        if key in self:
            raise self.ExistingPipe(key)
        self._add(key, pipe)

    def __bool__(self):
        """
        All pipes are ready
        """
        return (not self.missing()) and all(self.__pipes.values())


class Pipes(AbstractPipes):
    def __init__(self, *expects):
        super().__init__()
        self.__expects = tuple(expects)

    def expects(self, key):
        return key in self.__expects

    def missing(self):
        return len(self) < len(self.__expects)


class NoPipe(AbstractPipes):
    def expects(self, key):
        return False

    def missing(self):
        return False


class OnePipe(AbstractPipes):
    def expects(self, key):
        return key is None

    def missing(self):
        return None not in self

    def get(self):
        return self[None]

    def set(self, pipe: Pipe):
        self[None] = pipe


class AnyPipe(AbstractPipes):
    def expects(self, key):
        return True

    def missing(self):
        return False
