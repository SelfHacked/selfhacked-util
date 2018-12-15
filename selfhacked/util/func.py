from functools import wraps


def returns(type):
    def __decor(func):
        @wraps(func)
        def __new_func(*args, **kwargs):
            return type(func(*args, **kwargs))

        return __new_func

    return __decor
