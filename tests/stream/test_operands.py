import pytest

from selfhacked.stream import IterStream, Stream
from selfhacked.stream.io import FileStream
from selfhacked.stream.operands import (
    strip, remove_empty, remove_comments,
    decode, split_lines,
)


def test_or():
    s1 = IterStream('123')
    s2 = s1 | strip
    assert isinstance(s2, Stream)


@pytest.mark.dependency(
    depends=[
        'test_or',
        ('session', 'tests/stream/test_streams.py::test_file_stream'),
    ],
)
def test_strip(tmpdir):
    file = tmpdir / '0.txt'
    file.write_text("""123
abc
""", encoding='utf-8')

    assert tuple(FileStream(str(file)) | strip) == ('123', 'abc')


@pytest.mark.dependency(
    depends=[
        'test_or',
        ('session', 'tests/stream/test_streams.py::test_iter_stream'),
    ],
)
def test_remove_emtpy():
    assert tuple(IterStream(('123', '', 'abc')) | remove_empty) == ('123', 'abc')


@pytest.mark.dependency(
    depends=[
        'test_or',
        ('session', 'tests/stream/test_streams.py::test_iter_stream'),
    ],
)
def test_remove_comments():
    assert tuple(IterStream(('#123', 'abc')) | remove_comments) == ('abc',)


@pytest.mark.dependency(
    depends=[
        'test_or',
        ('session', 'tests/stream/test_streams.py::test_file_stream'),
        'test_strip',
        'test_remove_empty',
        'test_remove_comments',
    ],
)
def test_chain(tmpdir):
    file = tmpdir / '0.txt'
    file.write_text("""#123

abc
""", encoding='utf-8')

    assert tuple(
        FileStream(str(file))
        | strip
        | remove_empty
        | remove_comments
    ) == ('abc',)


@pytest.mark.dependency(
    depends=[
        'test_or',
        ('session', 'tests/stream/test_streams.py::test_iter_stream'),
    ],
)
def test_decode():
    assert tuple(IterStream((b'abc', b'123')) | decode) == ('abc', '123')


@pytest.mark.dependency(
    depends=[
        'test_or',
        ('session', 'tests/stream/test_streams.py::test_iter_stream'),
    ],
)
def test_split_lines():
    assert tuple(IterStream((
        'abc\n\n123',
        '456\n',
        '789\n'
    )) | split_lines) == (
               'abc\n',
               '\n',
               '123456\n',
               '789\n'
           )
