import logging.config
import os

from raven import Client


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
SENTRY_DSN = os.environ.get('SENTRY_DSN', '')
SENTRY_CLIENT = Client(SENTRY_DSN) if SENTRY_DSN else None

logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    },
    'handlers': {
        'rotating_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': SENSE_LOG_PATH,
            'maxBytes': 10 * 1024 * 1024,
            'backupCount': 5,
            'formatter': 'default',
            'level': logging.INFO,
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': logging.DEBUG,
        },
    },
    'root': {
        'handlers': [
            'rotating_file',
            'console',
        ],
        'level': logging.DEBUG,
    },
})

# Sensors #####################################################################

ENVIRONMENTAL_SENSORS_INTERVAL = int(
    os.getenv('ENVIRONMENTAL_SENSORS_INTERVAL', 1)
)

INERTIAL_SENSORS_INTERVAL = int(
    os.getenv('INERTIAL_SENSORS_INTERVAL', 1)
)
