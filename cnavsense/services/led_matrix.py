import os

from zmqservices import services
from cnavconstants.servers import (
    LOCAL_LED_MATRIX_ADDRESS, LED_MATRIX_PORT_ADDRESS
)

from cnavsense import settings
from cnavsense.utils import sentry, logger


class LedMatrix(services.JsonrpcServerResource):

    def __init__(self, *args, **kwargs):
        super(LedMatrix, self).__init__(*args, **kwargs)

        self.driver = kwargs.pop('driver', settings.SENSE_HAT_DRIVER)

        self.allowed_methods = {
            'set_rotation': self.validate_set_rotation_params,
            'set_pixels': self.validate_set_pixels_params,
            'set_pixel': self.validate_set_pixel_params,
            'get_pixel': self.validate_get_pixel_params,
            'load_image': self.validate_load_image_params,
            'flip_horizontally': lambda x: True,
            'flip_vertically': lambda x: True,
            'clear': lambda x: True,
            'set_colour': self.validate_set_colour_params,
            'show_message': self.validate_text_and_back_colour_params,
            'show_letter': self.validate_text_and_back_colour_params,
            'set_low_light': (
                lambda x: True if (x is True or x is False) else False
            ),
        }

    @staticmethod
    def validate_set_rotation_params(params):
        return params.get('value') in (0, 90, 180, 270)

    def set_rotation(self, value):
        self.driver.set_rotation(value)

    def flip_horizontally(self):
        self.driver.flip_h()

    def flip_vertically(self):
        self.driver.flip_v()

    @staticmethod
    def pixel_is_valid(pixel):
        return len(pixel) == 3 and (
            all((
                (isinstance(colour, int) and colour in range(0, 255))
                for colour in pixel
            ))
        )

    @staticmethod
    def validate_set_pixels_params(params):
        pixels = params.get('pixels')
        return (len(pixels) == 64) and [
            pixel for pixel in pixels if LedMatrix.pixel_is_valid(pixel)
        ]

    def set_pixels(self, pixels):
        if self.pixels_are_valid(pixels):
            self.driver.set_pixels(pixels)
        else:
            logger.error('Invalid pixels provided: "{}"'.format(pixels))

    def get_pixels(self):
        return self.driver.get_pixels()

    @staticmethod
    def validate_set_pixel_params(params):
        valid_range = range(0, 7)
        xy = params.get('x') in valid_range and params.get('y') in valid_range

        return xy and LedMatrix.pixel_is_valid(params.get('pixel'))

    def set_pixel(self, x, y, pixel):
        return self.driver.set_pixel(x, y, pixel)

    @staticmethod
    def validate_get_pixel_params(params):
        valid_range = range(0, 7)
        return (
            params.get('x') in valid_range and params.get('y') in valid_range
        )

    def get_pixel(self, x, y):
        return self.driver.get_pixel(x, y)

    @staticmethod
    def valid_path(path):
        return os.path.exists(path)

    @staticmethod
    def validate_load_image_params(params):
        return os.path.exists(params.get('file_path'))

    def load_image(self, file_path):
        return self.driver.load_image(file_path)

    def clear(self):
        self.driver.clear()

    @staticmethod
    def validate_set_colour_params(params):
        return LedMatrix.pixel_is_valid(params.get('pixel'))

    def set_colour(self, colour):
        self.driver.clear(colour)

    @staticmethod
    def validate_text_and_back_colour_params(params):
        return all((
            LedMatrix.pixel_is_valid(p) for p in (
                params.get('text_colour'), params.get('back_colour')
            )
        ))

    def show_message(
            self, text, scroll_speed=0.1,
            text_colour=(255, 255, 255), back_colour=(0, 0, 0)):

        self.driver.show_message(
            text,
            scroll_speed=scroll_speed,
            text_colour=text_colour,
            back_colour=back_colour,
        )

    def show_letter(
            self, letter, text_colour=(255, 255, 255), back_colour=(0, 0, 0)):

        self.driver.show_letter(
            letter, text_colour=text_colour, back_colour=back_colour
        )
        logger.error('Invalid pixels provided: "{}, {}"'.format(
            text_colour, back_colour
        ))

    def set_low_light(self, on=True):
        self.driver.low_light = on


class Service(services.JsonrpcServer):
    name = 'led_matrix'
    resource = LedMatrix
    address = LOCAL_LED_MATRIX_ADDRESS
    port = LED_MATRIX_PORT_ADDRESS


@sentry
def start():
    return Service()


if __name__ == '__main__':
    start()
