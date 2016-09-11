import mock

from cnavsense.services import environmental


class TestSensors(object):
    sensors = environmental.Sensors(driver=mock.Mock(), publisher=mock.Mock())

    def test_humidity(self):
        self.sensors.humidity

    def test_temperature(self):
        self.sensors.temperature

    def test_pressure(self):
        self.sensors.pressure
