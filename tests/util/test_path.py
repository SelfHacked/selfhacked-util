import os

from selfhacked.util.path import mkdir, cd


def test_mkdir(tmp_path):
    path = str(tmp_path)
    mkdir(path, 'a', 'b', 'c')
    assert os.path.isdir(os.path.join(path, 'a', 'b', 'c'))


def test_cd(tmp_path):
    os.chdir(str(tmp_path))
    path = os.path.abspath(os.getcwd())
    target = os.path.join(path, 'a')
    os.mkdir(target)

    with cd(target):
        assert os.getcwd() == target
    assert os.getcwd() == path
