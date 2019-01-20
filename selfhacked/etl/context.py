from contextlib import contextmanager

__registry = []


class RegistryError(Exception):
    pass


class NoRegistry(RegistryError):
    def __init__(self):
        super().__init__("Please run in a `with` context.")


class MismatchRegistry(RegistryError):
    def __init__(self):
        super().__init__("Please run in the same `with` context.")


def get_node_registry(match=None):
    if not __registry:
        raise NoRegistry
    result = __registry[-1]
    if match is not None and match != result:
        raise MismatchRegistry
    return result


@contextmanager
def context(registry):
    __registry.append(registry)
    try:
        yield
    finally:
        __registry.pop(-1)
