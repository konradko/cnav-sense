import mock

from cnavsense.services import led_matrix


class TestLedMatrix(object):
    led_matrix = led_matrix.LedMatrix(driver=mock.Mock(), server=mock.Mock())

    def test_validate_no_params(self):
        self.led_matrix.validate_no_params({})

    def test_validate_set_rotation_params(self):
        self.led_matrix.validate_no_params(dict(value=90))

    def test_set_rotation(self):
        self.led_matrix.set_rotation(value=180)

    def test_flip_horizontally(self):
        self.led_matrix.flip_horizontally()

    def test_flip_vertically(self):
        self.led_matrix.flip_vertically()

    def test_pixel_is_valid(self):
        self.led_matrix.pixel_is_valid(pixel=(255, 255, 255))

    def test_validate_set_pixels_params(self):
        self.led_matrix.validate_set_pixels_params(dict(
            pixels=list((255, 255, 255) for x in xrange(64))
        ))

    def test_set_pixels(self):
        self.led_matrix.set_pixels(
            pixels=list((255, 255, 255) for x in xrange(64))
        )

    def test_get_pixels(self):
        self.led_matrix.get_pixels()

    def test_validate_set_pixel_params(self):
        self.led_matrix.validate_set_pixel_params(dict(
            x=1, y=7, pixel=(255, 255, 255)
        ))

    def test_set_pixel(self):
        self.led_matrix.set_pixel(x=1, y=7, pixel=(255, 255, 255))

    def test_validate_get_pixel_params(self):
        self.led_matrix.validate_get_pixel_params(dict(x=1, y=7))

    def test_get_pixel(self):
        self.led_matrix.get_pixel(x=1, y=7)

    def test_valid_path(self):
        self.led_matrix.valid_path('~')

    def test_validate_load_image_params(self):
        self.led_matrix.validate_load_image_params(dict(file_path='~'))

    def test_load_image(self):
        self.led_matrix.load_image(file_path='~')

    def test_clear(self):
        self.led_matrix.clear()

    def test_validate_set_colour_params(self):
        self.led_matrix.validate_set_colour_params(
            dict(colour=(255, 255, 255))
        )

    def test_set_colour(self):
        self.led_matrix.set_colour(colour=(255, 255, 255))

    def test_validate_text_and_back_colour_params(self):
        self.led_matrix.validate_text_and_back_colour_params(dict(
            text_colour=(255, 255, 255), back_colour=(0, 0, 0)
        ))

    def test_show_message(self):
        self.led_matrix.show_message(text='test')

    def test_show_letter(self):
        self.led_matrix.show_letter(letter='t')

    def test_set_low_light(self):
        self.led_matrix.set_low_light(True)
