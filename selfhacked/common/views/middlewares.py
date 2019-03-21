from django.http import HttpResponseBadRequest

from .exceptions import RequestParamNotFound


class ViewExceptionMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if isinstance(exception, RequestParamNotFound):
            return HttpResponseBadRequest(exception)
