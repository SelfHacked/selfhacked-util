import pytest

from selfhacked.etl.context import NoRegistry, context
from selfhacked.etl.node import AbstractNode
from selfhacked.etl.pipe import OnePipe, Pipe


class DummyNode(AbstractNode):
    INPUT_PIPES_CLASS = OnePipe
    OUTPUT_PIPES_CLASS = OnePipe

    def _run(self):
        pass


@pytest.mark.dependency(
    scope='session',
    depends=[
        'tests/etl/test_context.py::test_no_context',
        'tests/etl/test_context.py::test_context',
    ],
)
def test_context():
    with pytest.raises(NoRegistry):
        DummyNode()

    registry = []
    with context(registry.append):
        n = DummyNode()
        n.pipe()

    with pytest.raises(NoRegistry):
        n.pipe()
    with pytest.raises(NoRegistry):
        Pipe(None, None) | n

    assert registry == [n]


@pytest.mark.dependency(
    depends=[
        'test_context',
    ],
)
def test_ready():
    registry = []
    with context(registry.append):
        p = Pipe(None, None)
        n = DummyNode()
        p | n

    assert not n
    with pytest.raises(AbstractNode.InputNotReady):
        n.run()

    p.feed('123')
    assert n
    n.run()
