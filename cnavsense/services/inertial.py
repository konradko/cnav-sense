import time

from zmqservices import messages, services, pubsub
from cnavconstants.publishers import (
    LOCAL_INERTIAL_SENSORS_ADDRESS, INERTIAL_SENSORS_SERVICE_PORT
)
import cnavconstants.topics


from cnavsense import settings
from cnavsense.utils import sentry


class Sensors(services.PublisherResource):
    topics = {
        'orientation': cnavconstants.topics.ORIENTATION,
        'compass': cnavconstants.topics.COMPASS,
    }

    def __init__(self, *args, **kwargs):
        super(Sensors, self).__init__(*args, **kwargs)

        self.driver = kwargs.pop('driver', settings.SENSE_HAT_DRIVER)

    def run(self):
        with sentry():
            while True:
                time.sleep(settings.INERTIAL_SENSORS_INTERVAL)

                for topic in self.topics:
                    self.publisher.send(messages.JSON(
                        topic=self.topics[topic],
                        data=getattr(self, topic),
                    ))

    @property
    def orientation(self):
        self.driver.set_imu_config(
            compass_enabled=True,
            gyro_enabled=True,
            accel_enabled=True,
        )

        return {
            'radians': self.driver.get_orientation_radians(),
            'degrees': self.driver.get_orientation_degrees(),
        }

    @property
    def compass(self):
        return self.driver.get_compass()


class Service(services.PublisherService):
    name = 'inertial_sensors'
    resource = Sensors
    address = LOCAL_INERTIAL_SENSORS_ADDRESS
    port = INERTIAL_SENSORS_SERVICE_PORT
    publisher = pubsub.LastMessagePublisher
    subscriber = pubsub.LastMessageSubscriber


def start():
    return Service().start()


if __name__ == '__main__':
    start()
