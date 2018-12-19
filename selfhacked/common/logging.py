import os

from selfhacked.util.path import mkdir


def add_rotating_handler(
        LOGGING: dict, BASE_DIR: str,
        namespace: str,
        name: str = None,
        path: str = None,
        formatter: str = None,
        propagate: bool = False,
        level: str = 'INFO',
        **logger_options,
):
    """
    E.g.

            add_rotating_handler(
                LOGGING, BASE_DIR,
                'django.server',
            )
            add_rotating_handler(
                LOGGING, BASE_DIR,
                'django.db',
                level='DEBUG',
            )
    """
    if name is None:
        name = namespace
    if path is None:
        path = os.path.join(BASE_DIR, 'logs', f"{name}.log")
    mkdir(os.path.dirname(path))

    handler = {
        'class': 'logging.handlers.TimedRotatingFileHandler',
        'filename': path,
        'when': 'midnight',
    }
    if formatter is not None:
        handler['formatter'] = formatter

    if 'handlers' not in LOGGING:
        LOGGING['handlers'] = {}
    LOGGING['handlers'][name] = handler

    logger = {
        'handlers': [name],
        'propagate': propagate,
        'level': level,
        **logger_options,
    }

    if 'loggers' not in LOGGING:
        LOGGING['loggers'] = {}
    LOGGING['loggers'][namespace] = logger
