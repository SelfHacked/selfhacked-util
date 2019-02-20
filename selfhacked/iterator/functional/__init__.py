def apply(func, *args, **kwargs):
    def __op(iterable):
        for item in iterable:
            yield func(item, *args, **kwargs)

    return __op


def remove_empty(iterable):
    for item in iterable:
        if not item:
            continue
        yield item
