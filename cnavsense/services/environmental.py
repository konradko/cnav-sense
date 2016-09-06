import time

from zmqservices import messages, services, pubsub

from cnavsense import settings
from cnavsense.utils import sentry


class Sensors(services.PublisherResource):
    topics = {
        'humidity': settings.HUMIDITY_TOPIC,
        'temperature': settings.TEMPERATURE_TOPIC,
        'pressure': settings.PRESSURE_TOPIC,
    }

    def __init__(self, *args, **kwargs):
        super(Sensors, self).__init__(*args, **kwargs)

        self.driver = kwargs.pop('driver', settings.SENSE_HAT_DRIVER)

    def run(self):
        while True:
            time.sleep(settings.ENVIRONMENTAL_SENSORS_INTERVAL)

            for topic in self.topics:
                self.publisher.send(messages.JSON(
                    topic=self.topics[topic],
                    data=getattr(self, topic),
                ))

    @property
    def humidity(self):
        return self.driver.get_humidity()

    @property
    def temperature(self):
        return {
            'from_humidity': self.driver.get_temperature_from_humidity(),
            'from_pressure': self.driver.get_temperature_from_pressure(),
        }

    @property
    def pressure(self):
        return self.driver.get_pressure()


class Service(services.PublisherService):
    name = 'environmental_sensors'
    resource = Sensors
    address = settings.LOCAL_ENVIRONMENTAL_SENSORS_PUBLISHER_ADDRESS
    port = settings.ENVIRONMENTAL_SENSORS_PORT_ADDRESS
    publisher = pubsub.LastMessagePublisher
    subscriber = pubsub.LastMessageSubscriber


@sentry
def start():
    return Service()


if __name__ == '__main__':
    start()