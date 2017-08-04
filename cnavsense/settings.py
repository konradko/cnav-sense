import logging.config
import os


PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

_, HOSTNAME, _, _, MACHINE = os.uname()
RUNNING_ON_PI = MACHINE.startswith('arm')

# Sense HAT ###################################################################

ENVIRONMENTAL_SENSORS_INTERVAL = float(
    os.getenv('ENVIRONMENTAL_SENSORS_INTERVAL', 0)
)

INERTIAL_SENSORS_INTERVAL = float(
    os.getenv('INERTIAL_SENSORS_INTERVAL', 0)
)

LED_MATRIX_DEFAULT_TEXT_SCROLL_SPEED = float(
    os.getenv('LED_MATRIX_DEFAULT_TEXT_SCROLL_SPEED', 0.1)
)

# Drivers #####################################################################

# Driver libs can only be installed on RPi
if RUNNING_ON_PI:
    from sense_hat import SenseHat  # noqa

    SENSE_HAT_DRIVER = SenseHat()
else:
    SENSE_HAT_DRIVER = None


# Services  ###################################################################
ENVIRONMENTAL_SERVICE_ENABLED = os.getenv(
    'ENVIRONMENTAL_SERVICE_ENABLED', 'false'
)
if ENVIRONMENTAL_SERVICE_ENABLED == 'true':
    ENVIRONMENTAL_SERVICE_ENABLED = True
else:
    ENVIRONMENTAL_SERVICE_ENABLED = False


INERTIAL_SERVICE_ENABLED = os.getenv(
    'INERTIAL_SERVICE_ENABLED', 'true'
)
if INERTIAL_SERVICE_ENABLED == 'true':
    INERTIAL_SERVICE_ENABLED = True
else:
    INERTIAL_SERVICE_ENABLED = False


JOYSTICK_SERVICE_ENABLED = os.getenv(
    'JOYSTICK_SERVICE_ENABLED', 'true'
)
if JOYSTICK_SERVICE_ENABLED == 'true':
    JOYSTICK_SERVICE_ENABLED = True
else:
    JOYSTICK_SERVICE_ENABLED = False


LED_MATRIX_SERVICE_ENABLED = os.getenv(
    'LED_MATRIX_SERVICE_ENABLED', 'true'
)
if LED_MATRIX_SERVICE_ENABLED == 'true':
    LED_MATRIX_SERVICE_ENABLED = True
else:
    LED_MATRIX_SERVICE_ENABLED = False


# Logging #####################################################################

SENSE_LOG_PATH = os.environ.get('SENSE_LOG_PATH', '/tmp/cnavsense.log')
SENTRY_DSN = os.environ.get('SENTRY_DSN')

logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'sentry': {
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
            'formatter': 'sentry',
        },
        'papertrail': {
            'class': 'logging.handlers.SysLogHandler',
            'formatter': 'default',
            'address': (
                os.getenv('PAPERTRAIL_HOST'),
                int(os.getenv('PAPERTRAIL_PORT', 0))
            ),
            'level': 'INFO',
        }
    },
    'root': {
        'handlers': [
            'rotating_file',
            'console',
            'sentry',
            'papertrail',
        ],
        'level': 'DEBUG',
        'propagate': True,
    },
})
