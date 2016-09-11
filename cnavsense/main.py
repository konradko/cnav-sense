import os
import sys

sys.path.append(os.getcwd())

from zmqservices import messages

from cnavsense import settings
from cnavsense.utils import log_exceptions, logger
from cnavsense.services import environmental, inertial, joystick, led_matrix


def run():
    logger.info("Starting...")

    environmental_service = environmental.Service()
    environmental_service.start()

    inertial_service = inertial.Service()
    inertial_service.start()

    joystick_service = joystick.Service()
    joystick_service.start()

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
