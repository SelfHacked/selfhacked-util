import pytest

from selfhacked.etl.pipe import (
    Pipe,
    NoPipe, OnePipe, Pipes, AnyPipe,
)


def test_no_pipe():
    pipes = NoPipe()
    assert not pipes.expects(None)
    assert not pipes.expects('hello')
    assert not pipes.missing()


def test_one_pipe():
    pipes = OnePipe()
    assert pipes.expects(None)
    assert not pipes.expects('hello')
    assert pipes.missing() == {None}

    pipes.set(Pipe(None, None))
    assert not pipes.missing()


def test_pipes():
    pipes = Pipes('a', 'b')
    assert not pipes.expects(None)
    assert pipes.expects('a')
    assert pipes.expects('b')
    assert not pipes.expects('hello')

    assert pipes.missing() == {'a', 'b'}
    pipes['a'] = Pipe(None, None)
    assert pipes.missing() == {'b'}
    pipes['b'] = Pipe(None, None)
    assert not pipes.missing()


def test_any_pipe():
    pipes = AnyPipe()
    assert pipes.expects(None)
    assert pipes.expects('hello')
    assert not pipes.missing()


def test_unexpected():
    pipes = Pipes('a', 'b')
    with pytest.raises(Pipes.UnexpectedPipe):
        pipes['hello'] = Pipe(None, None)


def test_existing():
    pipes = Pipes('a', 'b')
    pipes['a'] = Pipe(None, None)
    with pytest.raises(Pipes.ExistingPipe):
        pipes['a'] = Pipe(None, None)
    pipes['b'] = Pipe(None, None)


@pytest.mark.dependency(
    scope='session',
    depends=[
        'tests/etl/test_pipe.py::test_pipe_status',
    ],
)
def test_ready():
    pipes = Pipes('a', 'b')
    assert not pipes
    pipes['a'] = Pipe(None, None)
    assert not pipes
    pipes['a'].feed('123')
    assert not pipes
    pipes['b'] = Pipe(None, None)
    assert not pipes
    pipes['b'].feed('456')
    assert pipes
