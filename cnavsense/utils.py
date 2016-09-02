import logging.config

from cnavsense import settings


logger = logging.getLogger()


def sentry(func):
    """
    Decorator that sends exceptions to app.getsentry.com if SENTRY_DSN env var
    is set.
    """
    def wrapped(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            if settings.SENTRY_CLIENT:
                # prints traceback
                logging.exception("Exception occurred, sending to Sentry:")
                settings.SENTRY_CLIENT.captureException()
            else:
                raise
    return wrapped
