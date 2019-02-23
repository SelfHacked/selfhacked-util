import gzip
from typing import Iterable

from . import apply
from ..io import BytesIterableAsIO

decode = apply(bytes.decode, encoding='utf-8')


def un_gzip(iterable: Iterable[bytes]):
    readable = BytesIterableAsIO(iterable)
    with gzip.open(readable) as f:
        yield from f
