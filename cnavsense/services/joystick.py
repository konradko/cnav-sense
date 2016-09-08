from zmqservices import messages, services, pubsub
from cnavconstants.publishers import (
    LOCAL_JOYSTICK_ADDRESS, JOYSTICK_SERVICE_PORT
)
import cnavconstants.topics


from cnavsense import settings
from cnavsense.utils import sentry


class Joystick(services.PublisherResource):
    topics = {
        'joystick': cnavconstants.topics.JOYSTICK,
    }

    def __init__(self, *args, **kwargs):
        super(Joystick, self).__init__(*args, **kwargs)

        self.driver = kwargs.pop('driver', settings.SENSE_HAT_DRIVER)

    def run(self):
        while True:
            input_event = self.driver.stick.wait_for_event(emptybuffer=True)

            self.publisher.send(messages.JSON(
                topic=self.topics['joystick'],
                data=self.format_event(input_event),
            ))

    @staticmethod
    def format_event(event):
        return {
            'timestamp': event.timestamp,
            'direction': event.direction,
            'action': event.action,
        }


class Service(services.PublisherService):
    name = 'joystick'
    resource = Joystick
    address = LOCAL_JOYSTICK_ADDRESS
    port = JOYSTICK_SERVICE_PORT
    publisher = pubsub.Publisher
    subscriber = pubsub.Subscriber


@sentry
def start():
    return Service()


if __name__ == '__main__':
    start()
