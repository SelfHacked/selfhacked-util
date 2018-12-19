import os

from selfhacked.util.path import mkdir


def test_mkdir(tmp_path):
    path = str(tmp_path)
    mkdir(path, 'a', 'b', 'c')
    assert os.path.isdir(os.path.join(path, 'a', 'b', 'c'))
