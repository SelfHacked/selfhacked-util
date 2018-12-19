import os
from contextlib import contextmanager


def mkdir(path, *paths):
    """
    Recursively create a directory,
    equivalent of `mkdir -p`
    """

    path = os.path.join(path, *paths)
    if os.path.isfile(path):
        raise ValueError(f"Cannot make dir: '{path}' is a file")
    elif os.path.isdir(path):
        return
    basedir = os.path.dirname(path)
    mkdir(basedir)
    os.mkdir(path)


@contextmanager
def cd(path):
    cwd = os.path.abspath(os.getcwd())
    target = os.path.abspath(path)
    os.chdir(target)
    try:
        yield
    finally:
        os.chdir(cwd)
