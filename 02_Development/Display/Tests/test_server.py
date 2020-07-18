import unittest

from sensors import Sensors
import server

class TestServer(unittest.TestCase):

    def setUp(self):
        self._sensors = Sensors()
        self._data = self._sensors.poll()

    def tearDown(self):
        self._sensors.close()

    def test_poll_sensors_nominal(self):
        self.assertTrue(len(self._data[0]) == 2,
                        "Fails to generate exactly 1 pressure datum "
                        "and 1 flow rate datum for a patient.")

    def test_calculator_adds_and_gets_data(self):
        calculator = server.Calculator()
        calculator.add_datum(self._data)
        self.assertIn("PEEP", calculator.get_datum()[1],
                      "Fails to add data to and then get data from "
                      "the calculator.")
