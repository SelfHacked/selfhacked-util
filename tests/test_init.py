import pytest


def test():
    assert True


@pytest.mark.dependency()
def test_dependency():
    assert True


@pytest.mark.dependency(
    depends=['test_dependency'],
)
def test_depend():
    assert True
