import pytest


def test():
    assert True


def test_dependency():
    assert True


@pytest.mark.dependency(
    depends=['test_dependency'],
)
def test_depend():
    assert True
