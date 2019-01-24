import pytest

from selfhacked.etl.base.context import Context


def test_no_context():
    with pytest.raises(Context.NoContext):
        Context.get_context()
    with pytest.raises(Context.NoContext):
        Context.check_context(Context())


def test_context():
    ct = Context()
    with ct.context():
        assert Context.get_context() == ct


def test_check():
    ct = Context()
    with ct.context():
        with pytest.raises(Context.Mismatch):
            Context.check_context(Context())


@pytest.mark.dependency(
    depends=[
        'test_context',
    ],
)
def test_new():
    with Context.new_context() as ct:
        assert isinstance(ct, Context)
        assert Context.get_context() == ct


@pytest.mark.dependency(
    depends=[
        'test_new',
        'test_no_context',
    ],
)
def test_multiple():
    with Context.new_context() as ct0:
        assert Context.get_context() == ct0
        with Context.new_context() as ct1:
            assert Context.get_context() == ct1
        assert Context.get_context() == ct0
    with pytest.raises(Context.NoContext):
        Context.get_context()


@pytest.mark.dependency(
    depends=[
        'test_context',
    ],
)
def test_items():
    ct = Context()
    with ct.context():
        ct(0)

    assert tuple(ct.get_items(int)) == (0,)
