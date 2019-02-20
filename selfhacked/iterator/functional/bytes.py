import gzip
from typing import Iterable

from . import apply
from ..tools import ReadableIterator

decode = apply(bytes.decode, encoding='utf-8')


def un_gzip(iterable: Iterable[bytes]):
    readable = ReadableIterator(iter(iterable), b'')
    yield from gzip.open(readable)
