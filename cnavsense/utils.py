from contextlib import contextmanager
import logging.config

import raven

from cnavsense import settings


logger = logging.getLogger()


@contextmanager
def sentry():
    try:
        yield
    except:
        if settings.SENTRY_DSN:
            # prints traceback
            logging.exception("Exception occurred, sending to Sentry:")
            raven.Client(settings.SENTRY_DSN).captureException()
        else:
            raise
