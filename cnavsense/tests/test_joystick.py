import mock

from cnavsense.services import joystick


class TestJoystick(object):
    joystick = joystick.Joystick(driver=mock.Mock(), publisher=mock.Mock())

    def test_format_event(self):
        self.joystick.format_event(event=mock.Mock())
