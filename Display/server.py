import sys
import time
import json
import random

import zmq

from patienttubingdescriptorcalculator \
    import PatientTubingDescriptorCalculator

def poll_sensors(number_of_patients):
    """Pulls data from the pressure and flow sensors"""

    # placeholder
    while True:    
        yield tuple((random.uniform(0, 1), random.uniform(0, 1))
                    for _ in range(number_of_patients))


class Calculator():


    def __init__(self, number_of_patients):

        self._calculators = tuple(PatientTubingDescriptorCalculator()
                                  for _ in range(number_of_patients))

    def add_datum(self, datum):

        _datum = next(datum)
        if any(len(tubeSensor) != 2 for tubeSensor in _datum):
            raise(IndexError)
        for i in range(len(self._calculators)):
            self._calculators[i].add_flow_rate_datum(next(datum)[i][0])
            self._calculators[i].add_pressure_datum(next(datum)[i][1])

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

    NUMBER_OF_PATIENTS = 4
    sensor_data = poll_sensors(NUMBER_OF_PATIENTS)
    calculator = Calculator(NUMBER_OF_PATIENTS)
    communicator = Communicator()
    running = True
    while running:
        try:
            calculator.add_datum(sensor_data)

            communicator.publish_message(calculator.get_datum())
            time.sleep(1.0)
        except:
            running = False
            raise

if "__main__" == __name__:

    main()
