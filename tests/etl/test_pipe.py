import pytest
from typing import Dict, Any

from selfhacked.etl.pipe import Pipe


class DummyNode(object):
    def __init__(self):
        self.pipes: Dict[Any, Pipe] = {}

    def add_input(self, pipe, key):
        pass

    def pipe(self, key):
        if key not in self.pipes:
            self.pipes[key] = Pipe(self, key)
        return self.pipes[key]


def test_pipe_keys():
    node1 = DummyNode()

    node2 = DummyNode()
    node1.pipe(None) | node2
    assert node1.pipe(None).upstream == (node1, None)
    assert node1.pipe(None).downstream == (node2, None)

    node3 = DummyNode()
    node2.pipe('hello') | (node3, 'world')
    assert node2.pipe('hello').upstream == (node2, 'hello')
    assert node2.pipe('hello').downstream == (node3, 'world')


def test_used_pipe():
    node1 = DummyNode()
    node2 = DummyNode()
    node3 = DummyNode()

    node1.pipe(None) | node2
    with pytest.raises(Pipe.UsedPipe):
        node1.pipe(None) | node3


def test_pipe_status():
    p = Pipe(None, None)
    assert p.status == p.STATUS_SETUP
    assert p.accepts_feed
    assert not p
    with pytest.raises(p.PipeNotReady):
        tuple(p)

    p.feed('123')
    assert p.status == p.STATUS_READY
    assert not p.accepts_feed
    assert p
    with pytest.raises(p.PipeNotAcceptingFeed):
        p.feed('456')

    tuple(p)
    assert p.status == p.STATUS_USED
    assert not p.accepts_feed
    assert not p
    with pytest.raises(p.PipeNotReady):
        tuple(p)
    with pytest.raises(p.PipeNotAcceptingFeed):
        p.feed('789')


def test_pipe():
    p = Pipe(None, None)
    p.feed('123')
    assert tuple(p) == tuple('123')
