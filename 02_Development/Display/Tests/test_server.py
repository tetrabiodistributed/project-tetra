import unittest

from sensors import Sensors
import server


class TestServer(unittest.TestCase):

    def testPollSensors_nominal(self):
        sensors = Sensors()
        data = sensors.poll()
        self.assertTrue(len(data[0]) == 2,
                        "Fails to generate exactly 1 pressure datum "
                        "and 1 flow rate datum for a patient.")

    def testCalculator_adds_and_gets_data(self):
        sensors = Sensors()
        data = sensors.poll()
        calculator = server.Calculator()
        calculator.add_datum(data)
        self.assertIn("PEEP", calculator.get_datum()[0],
                      "Fails to add data to and then get data from "
                      "the calculator.")
