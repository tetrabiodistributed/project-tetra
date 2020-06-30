import sys
import time
import json
import random

import zmq

from patienttubingdescriptorcalculator \
    import PatientTubingDescriptorCalculator
from sensors import Sensors
import constants


class Calculator():


    def __init__(self):

        self._calculators = \
            tuple(PatientTubingDescriptorCalculator()
                  for _ in range(constants.NUMBER_OF_PATIENTS))

    def add_datum(self, datum):
        for i in range(len(self._calculators)):
            self._calculators[i].add_flow_rate_datum(datum[i][0])
            self._calculators[i].add_pressure_datum(datum[i][1])

    def get_datum(self):
        datum = {}
        for i in range(len(self._calculators)):
            datum.update({i: self._calculators[i].descriptors})
        return datum


class Communicator():

    def __init__(self, port=5000):
        self._socket = zmq.Context().socket(zmq.PUB)
        self._socket.bind(f"tcp://*:{port}")

    def publish_message(self, message):
        self._socket.send_multipart([b"",
                                     json.dumps(message).encode("ascii")])


def main():
    sensors = Sensors(constants.PRESSURE_SAMPLING_RATE,
                      constants.PRESSURE_OVERSAMPLING,
                      constants.TEMPERATURE_SAMPLING_RATE,
                      constants.TEMPERATURE_OVERSAMPLING)
    sensor_data = sensors.poll_sensors()
    calculator = Calculator()
    communicator = Communicator()
    running = True
    while running:
        try:
            calculator.add_datum(next(sensor_data))

            communicator.publish_message(calculator.get_datum())
            time.sleep(1.0)
        except:
            running = False
            raise


if "__main__" == __name__:
    main()
