from io import SEEK_CUR

import pytest

from selfhacked.io import BytesIterableAsIO


def get() -> BytesIterableAsIO:
    return BytesIterableAsIO([b'123\n45\n\n6\n'])


def test_readonly():
    f = get()
    assert f.readable()
    assert not f.writable()
    with pytest.raises(OSError):
        f.write(b'0')
    with pytest.raises(OSError):
        f.writelines([b'1', b'2'])
    with pytest.raises(OSError):
        f.flush()


def test_read():
    f = get()
    assert f.read(0) == b''
    assert f.read(1) == b'1'
    assert f.read(3) == b'23\n'
    assert f.read() == b'45\n\n6\n'


def test_readline():
    f = get()
    assert f.readline(0) == b''
    assert f.readline(1) == b'1'
    assert f.readline() == b'23\n'
    assert f.readline(100) == b'45\n'


def test_readlines():
    f = get()
    assert f.readlines(0) == []
    assert f.readlines(1) == [b'123\n']
    assert f.readlines(2) == [b'45\n', b'\n']
    assert f.readlines() == [b'6\n']


def test_iter():
    f = get()
    assert next(f) == b'123\n'
    assert tuple(f) == (b'45\n', b'\n', b'6\n')


@pytest.mark.dependency(
    depends=['test_read'],
)
def test_tell():
    f = get()
    assert f.tell() == 0
    f.read(1)
    assert f.tell() == 1
    f.read(3)
    assert f.tell() == 4
    f.read()
    assert f.tell() == 10


def test_seekable():
    f = get()
    assert f.seekable()
    with pytest.raises(OSError):
        f.truncate()


def test_seek_forward_only():
    f = get()
    with pytest.raises(OSError):
        f.seek(0, 2)
    f.seek(2)
    with pytest.raises(OSError):
        f.seek(0, 0)
    with pytest.raises(OSError):
        f.seek(-1, 1)


@pytest.mark.dependency(
    depends=[
        'test_read',
        'test_tell',
    ],
)
def test_seek():
    f = get()
    f.seek(2)
    assert f.tell() == 2
    assert f.read(1) == b'3'
    f.seek(2, SEEK_CUR)
    assert f.tell() == 5
    assert f.read(1) == b'5'


def test_os():
    f = get()
    assert f.mode == 'rb'
    assert not f.closed
    with pytest.raises(OSError):
        f.fileno()
    assert not f.isatty()


def test_with():
    with get() as f:
        pass
