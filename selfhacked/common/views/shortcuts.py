from .exceptions import RequestParamNotFound


def get_param_or_400(method, param):
    """
    E.g.

        get_param_or_400(request.GET, 'q')

    Must be used in conjunction with ViewExceptionMiddleware
    """

    try:
        return method[param]
    except KeyError:
        raise RequestParamNotFound(param)
