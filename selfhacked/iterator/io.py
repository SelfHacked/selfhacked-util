from io import SEEK_SET, SEEK_END
from typing import Iterable, Iterator, BinaryIO, List

from selfhacked.util.func import returns
from . import yield_from


class BytesIterableAsIO(BinaryIO):
    NEWLINE = 10  # b'\n'

    ERROR = OSError

    def __init__(self, iterable: Iterable[bytes]):
        self.__iter = yield_from(iterable)
        self.__pointer = 0

    # --- read ---

    def readable(self) -> bool:
        return True

    @returns(bytes)
    def __read(self, *, n=None, line=False) -> bytes:
        i = 0
        while True:
            if n is not None and i >= n:
                return
            try:
                b = next(self.__iter)
            except StopIteration:
                return
            yield b
            i += 1
            self.__pointer += 1
            if line and b == self.NEWLINE:
                return

    def read(self, n: int = -1) -> bytes:
        if n == -1:
            n = None
        return self.__read(n=n, line=False)

    def readline(self, limit: int = -1) -> bytes:
        if limit == -1:
            limit = None
        return self.__read(n=limit, line=True)

    def __readlines(self, *, n=None) -> Iterable[bytes]:
        i = 0
        while True:
            if n is not None and i >= n:
                return
            line = self.readline()
            if not line:
                return
            yield line
            i += 1

    def readlines(self, hint: int = -1) -> List[bytes]:
        if hint == -1:
            hint = None
        return list(self.__readlines(n=hint))

    def __next__(self) -> bytes:
        return next(iter(self.__readlines(n=1)))

    def __iter__(self) -> Iterator[bytes]:
        return iter(self.__readlines())

    # --- seek ---

    def seekable(self) -> bool:
        return True

    def tell(self) -> int:
        return self.__pointer

    def seek(self, offset: int, whence: int = SEEK_SET):
        if whence == SEEK_END:
            raise self.ERROR
        if whence == SEEK_SET:
            if offset < self.__pointer:
                raise self.ERROR
            offset = self.__pointer + offset
        if offset < 0:
            raise self.ERROR
        self.__read(n=offset)

    def truncate(self, size: int = None):
        raise self.ERROR

    # --- os ---

    @property
    def mode(self) -> str:
        return 'rb'

    def __enter__(self) -> BinaryIO:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def close(self) -> None:
        pass

    @property
    def closed(self) -> bool:
        return False

    def fileno(self) -> int:
        raise self.ERROR

    @property
    def name(self) -> str:
        return str(self)

    def isatty(self) -> bool:
        return False

    # --- not writable ---

    def writable(self) -> bool:
        return False

    def write(self, s: bytes) -> None:
        raise self.ERROR

    def writelines(self, lines: List[bytes]) -> None:
        raise self.ERROR

    def flush(self) -> None:
        raise self.ERROR
