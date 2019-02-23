import gzip
import pytest

from selfhacked.iterator.functional.bytes import un_gzip
from selfhacked.iterator.stream.io import FileStream


@pytest.mark.dependency(
    scope='session',
    depends=[
        'tests/iterator/test_streams.py::test_file_stream',
        'tests/iterator/test_streams.py::test_or',
        'tests/iterator/test_tools.py::test_readable_read',
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
