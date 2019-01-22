import pytest

from selfhacked.etl.context import Context
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
        'tests/etl/test_context.py::test_items',
    ],
)
def test_context():
    with pytest.raises(Context.NoContext):
        DummyNode()

    context = Context()
    with context.context():
        n = DummyNode()
        n.pipe()

    with pytest.raises(Context.NoContext):
        n.pipe()
    with pytest.raises(Context.NoContext):
        Pipe(None, None) | n

    assert tuple(context.get_items(DummyNode)) == (n,)


@pytest.mark.dependency(
    depends=[
        'test_context',
    ],
)
def test_ready():
    with Context.new_context():
        p = Pipe(None, None)
        n = DummyNode()
        p | n

    assert not n
    with pytest.raises(AbstractNode.InputNotReady):
        n.run()

    p.feed('123')
    assert n
    n.run()
