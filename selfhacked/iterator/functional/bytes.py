import gzip
from typing import Iterable, Iterator

from . import apply
from ..io import BytesIterableAsIO

decode = apply(bytes.decode, encoding='utf-8')


def un_gzip(iterable: Iterable[bytes]) -> Iterator[str]:
    """
    Unzip a gzip byte stream into str, and split by lines.
    """
    readable = BytesIterableAsIO(iterable)
    with gzip.open(readable) as f:
        yield from f
