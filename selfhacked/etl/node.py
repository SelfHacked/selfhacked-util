from .context import Context
from .pipe import Pipe, AbstractPipes


class AbstractNode(object):
    INPUT_PIPES_CLASS = None
    OUTPUT_PIPES_CLASS = None

    def __init__(self):
        self.__context = Context.get_context()
        self.__context(self)

        self.__input_pipes = self._create_input_pipes()
        self.__output_pipes = self._create_output_pipes()

    def _check_context(self):
        Context.check_context(self.__context)

    def _create_input_pipes(self) -> AbstractPipes:
        return self.INPUT_PIPES_CLASS()

    def _create_output_pipes(self) -> AbstractPipes:
        return self.OUTPUT_PIPES_CLASS()

    def add_input(self, pipe: Pipe, key=None):
        self._check_context()
        self.__input_pipes[key] = pipe

    def pipe(self, key=None):
        self._check_context()
        pipe = Pipe(self, key)
        self.__output_pipes[key] = pipe
        return pipe

    def __bool__(self):
        """
        Input pipes are ready
        """
        return bool(self.__input_pipes)

    def prepare(self):
        pass

    def _get_input(self, key):
        return self.__input_pipes[key]

    def _feed_output(self, key, iterable):
        self.__output_pipes[key].feed(iterable)

    def _run(self):
        raise NotImplementedError

    class InputNotReady(Exception):
        pass

    def run(self):
        if not self:
            raise self.InputNotReady
        self._run()

    def cleanup(self):
        pass
