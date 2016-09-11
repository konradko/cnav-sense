import logging.config
import os


PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

_, HOSTNAME, _, _, MACHINE = os.uname()
RUNNING_ON_PI = (
    HOSTNAME.startswith('raspberrypi') and MACHINE.startswith('arm')
)


# Drivers #####################################################################

# Driver libs can only be installed on RPi
if RUNNING_ON_PI:
    from sense_hat import SenseHat  # noqa

    SENSE_HAT_DRIVER = SenseHat()
else:
    SENSE_HAT_DRIVER = None


# Logging #####################################################################

SENSE_LOG_PATH = os.environ.get('SENSE_LOG_PATH', '/tmp/cnavsense.log')
SENTRY_DSN = os.environ.get('SENTRY_DSN')

logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': (
                '[%(asctime)s][%(levelname)s] %(name)s '
                '%(filename)s:%(funcName)s:%(lineno)d | %(message)s'
            ),
            'datefmt': '%H:%M:%S',
        }
    },
    'handlers': {
        'rotating_file': {
            'class': 'zmqservices.utils.MultiprocessingRotatingFileHandler',
            'filename': SENSE_LOG_PATH,
            'maxBytes': 10 * 1024 * 1024,
            'backupCount': 5,
            'formatter': 'default',
            'level': 'INFO',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': 'DEBUG',
        },
        'sentry': {
            'class': 'raven.handlers.logging.SentryHandler',
            'dsn': SENTRY_DSN,
            'level': 'ERROR',
        },
    },
    'root': {
        'handlers': [
            'rotating_file',
            'console',
            'sentry',
        ],
        'level': 'DEBUG',
    },
})


# Sensors #####################################################################

ENVIRONMENTAL_SENSORS_INTERVAL = float(
    os.getenv('ENVIRONMENTAL_SENSORS_INTERVAL', 0)
)

INERTIAL_SENSORS_INTERVAL = float(
    os.getenv('INERTIAL_SENSORS_INTERVAL', 0)
)
