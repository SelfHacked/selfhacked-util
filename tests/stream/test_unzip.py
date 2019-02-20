import gzip
import pytest

from selfhacked.stream.io import FileStream
from selfhacked.stream.operands import un_gzip


@pytest.mark.dependency(
    scope='session',
    depends=[
        'tests/stream/test_streams.py::test_file_stream',
        'tests/stream/test_operands.py::test_or',
        'tests/test_iterator.py::test_readable_read',
    ],
)
def test_un_gzip(tmpdir):
    file = str(tmpdir / '0.txt.gz')
    with gzip.open(file, mode='wb') as f:
        f.write(b"""#123

456
""")

    assert tuple(
        FileStream(file, binary=True)
        | un_gzip
    ) == (
               b'#123\n',
               b'\n',
               b'456\n',
           )
