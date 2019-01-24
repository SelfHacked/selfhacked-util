from typing import Iterator

from .setup import SetupCheck


class Pipe(Iterator, SetupCheck):
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

    def __init__(self, upstream, key):
        self.__upstream = upstream
        self.__upstream_key = key
        self.__downstream = None
        self.__downstream_key = None

        self.__status = self.STATUS_SETUP
        self.__iterable = None

    @property
    def upstream(self):
        return self.__upstream, self.__upstream_key

    def __or__(self, other):
        if self.connected:
            raise self.UsedPipe
        if isinstance(other, tuple):
            downstream, key = other
        else:
            downstream = other
            key = None
        self.__downstream = downstream
        self.__downstream_key = key
        downstream.add_input(self, key)

    @property
    def connected(self):
        return self.__downstream is not None

    @property
    def downstream(self):
        return self.__downstream, self.__downstream_key

    def setup_check(self):
        if not self.connected:
            raise self.SetupError(f"No downstream for pipe {self.upstream}")

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
    def ready(self):
        return self.status == self.STATUS_READY

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
