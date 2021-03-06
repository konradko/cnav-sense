import logging
import os

from zmqservices import services
from cnavconstants.servers import (
    LOCAL_LED_MATRIX_ADDRESS, LED_MATRIX_PORT_ADDRESS
)

from cnavsense import settings
from cnavsense.utils import log_exceptions


logger = logging.getLogger()


class LedMatrix(services.JsonrpcServerResource):

    def __init__(self, *args, **kwargs):
        super(LedMatrix, self).__init__(*args, **kwargs)

        self.driver = kwargs.pop('driver', settings.SENSE_HAT_DRIVER)

        self.endpoints = {
            'set_rotation': self.validate_set_rotation_params,
            'set_pixels': self.validate_set_pixels_params,
            'set_pixel': self.validate_set_pixel_params,
            'get_pixel': self.validate_get_pixel_params,
            'load_image': self.validate_load_image_params,
            'flip_horizontally': self.validate_no_params,
            'flip_vertically': self.validate_no_params,
            'clear': self.validate_no_params,
            'set_colour': self.validate_set_colour_params,
            'show_message': self.validate_text_and_back_colour_params,
            'show_letter': self.validate_text_and_back_colour_params,
            'set_low_light': (
                lambda x: True if (x is True or x is False) else False
            ),
        }

    def run(self, *args, **kwargs):
        with log_exceptions():
            super(LedMatrix, self).run(*args, **kwargs)

    @staticmethod
    def validate_no_params(params=None):
        return not params

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
        return pixel and (len(pixel) == 3 and (
            all((
                (isinstance(colour, int) and colour in range(0, 256))
                for colour in pixel
            ))
        ))

    @staticmethod
    def validate_set_pixels_params(params):
        pixels = params.get('pixels')
        return (len(pixels) == 64) and [
            pixel for pixel in pixels if LedMatrix.pixel_is_valid(pixel)
        ]

    def set_pixels(self, pixels):
        self.driver.set_pixels(pixels)

    def get_pixels(self):
        return self.driver.get_pixels()

    @staticmethod
    def validate_set_pixel_params(params):
        valid_range = range(1, 8)
        xy = params.get('x') in valid_range and params.get('y') in valid_range

        return xy and LedMatrix.pixel_is_valid(params.get('pixel'))

    def set_pixel(self, x, y, pixel):
        return self.driver.set_pixel(x, y, pixel)

    @staticmethod
    def validate_get_pixel_params(params):
        valid_range = range(1, 8)
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
        return LedMatrix.pixel_is_valid(params.get('colour'))

    def set_colour(self, colour):
        self.driver.clear(colour)

    @staticmethod
    def validate_text_and_back_colour_params(params):
        pixels = (params.get('back_colour'), params.get('text_colour'))

        return all((LedMatrix.pixel_is_valid(p) for p in pixels if p))

    def show_message(
            self, text,
            scroll_speed=settings.LED_MATRIX_DEFAULT_TEXT_SCROLL_SPEED,
            text_colour=(255, 255, 255), back_colour=(0, 0, 0)):

        self.driver.show_message(
            text,
            scroll_speed=scroll_speed,
            text_colour=text_colour,
            back_colour=back_colour,
        )
        self.clear()

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


def start():
    return Service().start()


if __name__ == '__main__':
    start()
