import logging
from django.db import connection

from selfhacked.util.func import timed

db_logger = logging.getLogger('django.db.debugging')


class SqlQueryCountMiddleWare(object):
    class Cursor(object):
        TIMED_METHOD = ['callproc', 'execute', 'executemany']

        def __init__(self, cursor, queries: list):
            self.cursor = cursor
            self.queries = queries

        def timed(self, method):
            return timed(self.queries.append)(method)

        def __getattr__(self, item):
            if item in self.TIMED_METHOD:
                method = self.timed(getattr(self.cursor, item))
                setattr(self, item, method)
                return method
            return getattr(self.cursor, item)

        def __iter__(self):
            return iter(self.cursor)

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            return self.close()

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        cursor = connection.cursor
        queries = []

        def new_cursor(*args, **kwargs):
            return self.Cursor(cursor(*args, **kwargs), queries)

        connection.cursor = new_cursor

        try:
            return self.get_response(request)
        finally:
            db_logger.debug(
                f"\"{request.method} {request.path}\" "
                f"{len(queries)} queries took {sum(queries)} seconds"
            )
