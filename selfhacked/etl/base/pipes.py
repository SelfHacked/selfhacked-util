from typing import Union, Set

from .pipe import Pipe
from .setup import SetupCheck


class AbstractPipes(SetupCheck):
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

    def missing(self) -> Union[Set[str], None]:
        """
        Return missing keys or None
        """
        raise NotImplementedError

    def setup_check(self):
        missing = self.missing()
        if missing:
            raise self.SetupError(f"Missing pipes: {missing}")

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
        return all(pipe.ready for pipe in self.__pipes.values())


class Pipes(AbstractPipes):
    def __init__(self, *expects):
        super().__init__()
        self.__expects = set(expects)

    def expects(self, key):
        return key in self.__expects

    def missing(self):
        return self.__expects.difference(self.keys())


class NoPipe(AbstractPipes):
    def expects(self, key):
        return False

    def missing(self):
        pass


class OnePipe(AbstractPipes):
    def expects(self, key):
        return key is None

    def missing(self):
        if None in self:
            return
        return {None}

    def get(self):
        return self[None]

    def set(self, pipe: Pipe):
        self[None] = pipe


class AnyPipe(AbstractPipes):
    def expects(self, key):
        return True

    def missing(self):
        pass
