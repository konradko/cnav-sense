from contextlib import contextmanager
import logging


@contextmanager
def log_exceptions():
    try:
        yield
    except:
        logging.exception('Exception: ')
        raise
