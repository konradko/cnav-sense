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

# Messaging ###################################################################

LOCAL_PUBLISHER_ADDRESS = 'tcp://localhost:{port}'
PUBLISHER_PORT_ADDRESS = 'tcp://*:{port}'

HUMIDITY_TOPIC = 'sense.humidity'
TEMPERATURE_TOPIC = 'sense.temperature'
PRESSURE_TOPIC = 'sense.pressure'
ENVIRONMENTAL_SENSORS_PORT = int(
    os.getenv('ENVIRONMENTAL_SENSORS_PORT', 48640)
)
LOCAL_ENVIRONMENTAL_SENSORS_PUBLISHER_ADDRESS = LOCAL_PUBLISHER_ADDRESS.format(
    port=ENVIRONMENTAL_SENSORS_PORT
)
ENVIRONMENTAL_SENSORS_PORT_ADDRESS = PUBLISHER_PORT_ADDRESS.format(
    port=ENVIRONMENTAL_SENSORS_PORT
)
ENVIRONMENTAL_SENSORS_INTERVAL = int(
    os.getenv('ENVIRONMENTAL_SENSORS_INTERVAL', 1)
)


ORIENTATION_TOPIC = 'sense.orientation'
COMPASS_TOPIC = 'sense.compass'
INERTIAL_SENSORS_PORT = int(
    os.getenv('INERTIAL_SENSORS_PORT', 48641)
)
LOCAL_INERTIAL_SENSORS_PUBLISHER_ADDRESS = LOCAL_PUBLISHER_ADDRESS.format(
    port=INERTIAL_SENSORS_PORT
)
INERTIAL_SENSORS_PORT_ADDRESS = PUBLISHER_PORT_ADDRESS.format(
    port=INERTIAL_SENSORS_PORT
)
INERTIAL_SENSORS_INTERVAL = int(
    os.getenv('INERTIAL_SENSORS_INTERVAL', 1)
)

JOYSTICK_INPUT_TOPIC = 'sense.joystick'
JOYSTICK_PORT = int(
    os.getenv('JOYSTICK_PORT', 48642)
)
LOCAL_JOYSTICK_PUBLISHER_ADDRESS = LOCAL_PUBLISHER_ADDRESS.format(
    port=JOYSTICK_PORT
)
JOYSTICK_PORT_ADDRESS = PUBLISHER_PORT_ADDRESS.format(
    port=JOYSTICK_PORT
)


LED_MATRIX_PORT = int(
    os.getenv('LED_MATRIX_PORT', 48643)
)
LOCAL_LED_MATRIX_ADDRESS = LOCAL_PUBLISHER_ADDRESS.format(
    port=LED_MATRIX_PORT
)
LED_MATRIX_PORT_ADDRESS = PUBLISHER_PORT_ADDRESS.format(
    port=LED_MATRIX_PORT
)
