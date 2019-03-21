from time import sleep

import pytest

from selfhacked.testing import assert_time


def test_assert_time():
    with assert_time(0.1):
        sleep(0.1)

    with pytest.raises(AssertionError):
        with assert_time(0.1):
            pass

    with pytest.raises(AssertionError):
        with assert_time(0):
            sleep(0.1)
