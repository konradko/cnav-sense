import mock

from cnavsense.services import inertial


class TestSensors(object):
    sensors = inertial.Sensors(driver=mock.Mock(), publisher=mock.Mock())

    def test_orientation(self):
        self.sensors.orientation

    def test_compass(self):
        self.sensors.compass
