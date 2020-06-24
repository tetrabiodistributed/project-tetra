import unittest

import zmq

import server

class TestServer(unittest.TestCase):


    def testPollSensors_nominal(self):

        self.assertTrue(len(next(server.poll_sensors(4))[0]) == 2,
                        "Fails to generate exactly 1 pressure datum "
                        "and 1 flow rate datum for a patient.")

    def testCalculator_adds_and_gets_data(self):

        calculator = server.Calculator(4)
        calculator.add_datum(server.poll_sensors(4))
        self.assertIn("PEEP", calculator.get_datum()[0],
                      "Fails to add data to and then get data from "
                      "the calculator.")

    def testCalculator_too_many_sensors(self):

        calculator = server.Calculator(4)
        with self.assertRaises(IndexError) as indexError:
            calculator.add_datum((tuple((1, 1, 1) for _ in range(4))
                                  for _ in range(10)))
        self.assertIsNotNone(indexError.exception,
                             "Fails to raise an exception when too "
                             "much sensor data is added to the "
                             "calculator.")
