import os
import sys

sys.path.append(os.getcwd())

from cnavsense import settings
from cnavsense.utils import sentry, logger
from cnavsense.services import environmental, inertial, joystick


@sentry
def run():
    logger.info("Starting...")

    environmental.Service().start()
    inertial.Service().start()
    joystick.Service().start()

    logger.info("Done")


if __name__ == '__main__':
    if settings.RUNNING_ON_PI:
        run()
    else:
        logger.warning("Not running on a Raspberry Pi")
