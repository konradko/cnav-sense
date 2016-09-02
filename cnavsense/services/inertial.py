import time

from zmqservices import messages, services, pubsub

from cnavsense import settings
from cnavsense.utils import sentry


class Sensors(services.PublisherResource):
    topics = {
        'orientation': settings.ORIENTATION_TOPIC,
        'compass': settings.COMPASS_TOPIC,
    }

    def __init__(self, *args, **kwargs):
        super(Sensors, self).__init__(*args, **kwargs)

        self.driver = kwargs.pop('driver', settings.SENSE_HAT_DRIVER)

    def run(self):
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
    address = settings.LOCAL_INERTIAL_SENSORS_PUBLISHER_ADDRESS
    port = settings.INERTIAL_SENSORS_PORT_ADDRESS
    publisher = pubsub.LastMessagePublisher
    subscriber = pubsub.LastMessageSubscriber


@sentry
def start():
    return Service()


if __name__ == '__main__':
    start()
