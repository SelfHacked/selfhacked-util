import os
import pytest

from selfhacked.util.path import mkdir, cd


def test_mkdir(tmpdir):
    path = str(tmpdir)
    mkdir(path, 'a', 'b', 'c')
    assert os.path.isdir(os.path.join(path, 'a', 'b', 'c'))


def test_file(tmpdir):
    (tmpdir / '0').write('abc')
    with pytest.raises(ValueError):
        mkdir(str(tmpdir), '0')


def test_cd(tmpdir):
    os.chdir(str(tmpdir))
    path = os.path.abspath(os.getcwd())
    target = os.path.join(path, 'd')
    os.mkdir(target)

    with cd(target):
        assert os.getcwd() == target
    assert os.getcwd() == path


@pytest.mark.dependency(
    depends=[
        'test_mkdir',
        'test_cd',
    ],
)
def test_mkdir_relative(tmpdir):
    with cd(str(tmpdir)):
        mkdir('e')
