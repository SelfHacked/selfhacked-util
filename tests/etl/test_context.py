import pytest

from selfhacked.etl.context import (
    get_node_registry, context,
    NoRegistry, MismatchRegistry,
)


def test_no_context():
    with pytest.raises(NoRegistry):
        get_node_registry()
    with pytest.raises(NoRegistry):
        get_node_registry(0)


def test_context():
    with context(0):
        assert 0 == get_node_registry()


def test_mismatch():
    with context(0):
        with pytest.raises(MismatchRegistry):
            get_node_registry(1)


@pytest.mark.dependency(
    depends=[
        'test_no_context',
        'test_context',
    ],
)
def test_multiple():
    with context(0):
        assert 0 == get_node_registry()
        with context(1):
            assert 1 == get_node_registry()
        assert 0 == get_node_registry()
    with pytest.raises(NoRegistry):
        get_node_registry()
