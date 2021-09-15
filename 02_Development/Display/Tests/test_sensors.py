import unittest
import time

from sensors import Sensors
import constants


class TestSensors(unittest.TestCase):

    def setUp(self):
        self._start_time = time.time()
        self._sensors = Sensors()

    def tearDown(self):
        self._sensors.close()

    def test_all_tubes_have_enough_sensors(self):
        tubes = self._sensors.tubes_with_enough_sensors()
        for i in range(constants.NUMBER_OF_PATIENTS):
            with self.subTest(i=i):
                self.assertIn(i, tubes,
                              f"Port {i} is missing sensors.")

    def test_calibration_pressure_sensor_present(self):
        self.assertTrue(self._sensors.calibration_pressure_sensor_connected(),
                        "Calibration pressure sensor is missing.")

    def test_poll_and_connected_sensors_are_same_shape(self):
        connected_sensors = self._sensors.connected_sensors()
        sensor_data = self._sensors.poll()
        for i in range(len(connected_sensors)):
            with self.subTest(i=i):
                self.assertEqual(len(connected_sensors[i]),
                                 len(sensor_data[i]),
                                 f"Contradicting shapes on port {i}.")
