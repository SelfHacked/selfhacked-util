import pytest

from selfhacked.iterator.functional import strip, remove_empty, remove_comments
from selfhacked.iterator.stream import IterStream, Stream
from selfhacked.iterator.stream.io import InputStream, FileStream


def test_iter_stream():
    s = IterStream('abc')
    assert tuple(s) == ('a', 'b', 'c')


def test_input_stream(monkeypatch):
    x = iter(['abc', '123'])

    def input():
        try:
            return next(x)
        except StopIteration:
            raise EOFError from None

    monkeypatch.setattr('builtins.input', input)
    s = InputStream()
    assert tuple(s) == ('abc', '123')


def test_file_stream(tmpdir):
    file = tmpdir / '0.txt'
    file.write_text("""123
abc
""", encoding='utf-8')
    s = FileStream(str(file))
    assert tuple(s) == ('123\n', 'abc\n')


def test_or():
    s1 = IterStream('123')
    s2 = s1 | strip
    assert isinstance(s2, Stream)


@pytest.mark.dependency(
    depends=[
        'test_or',
        'test_file_stream',
        ('session', 'tests/iterator/test_functional.py::test_strip'),
        ('session', 'tests/iterator/test_functional.py::test_remove_empty'),
        ('session', 'tests/iterator/test_functional.py::test_remove_comments'),
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
