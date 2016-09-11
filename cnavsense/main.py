import logging
import os
import sys

sys.path.append(os.getcwd())

from zmqservices import messages

from cnavsense import settings
from cnavsense.utils import log_exceptions
from cnavsense.services import environmental, inertial, joystick, led_matrix


logger = logging.getLogger()


def run():
    logger.info("Starting...")

    if settings.ENVIRONMENTAL_SERVICE_ENABLED:
        environmental.Service().start()

    if settings.INERTIAL_SERVICE_ENABLED:
        inertial.Service().start()

    if settings.JOYSTICK_SERVICE_ENABLED:
        joystick.Service().start()

    if settings.LED_MATRIX_SERVICE_ENABLED:
        led_matrix_service = led_matrix.Service()
        led_matrix_service.start()
        led_matrix_service.get_client().request(
            message=messages.JSON(data={'method': 'clear'})
        )

    logger.info("Done")


if __name__ == '__main__':
    with log_exceptions():
        if settings.RUNNING_ON_PI:
            run()
        else:
            logger.warning("Not running on a Raspberry Pi")
