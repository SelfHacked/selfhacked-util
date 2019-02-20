from selfhacked.stream import IterStream
from selfhacked.stream.io import InputStream, FileStream


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
