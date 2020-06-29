import sys
import time
import json
import random

import zmq

from patienttubingdescriptorcalculator \
    import PatientTubingDescriptorCalculator
import constants


class Sensors():
    """Dummy class while I work on the real thing"""

    def __init__(self, number_of_patients):
        self._number_of_patients = number_of_patients

    def connected_sensors(self, not_enough_sensors=False):
        if not_enough_sensors:
            # SPL06-007 = pressure sensor
            return tuple([("SPL06-007")]
                         .extend([("SPL06-007", "SFM3300")
                                  for _ in range(self._number_of_patients-1)]))
        else:
            return tuple(("SPL06-007", "SFM3300")
                         for _ in range(self._number_of_patients))

    def calibration_pressure_sensor_connected(self, fail=False):
        if fail:
            return False
        else:
            return True

    def tubes_with_enough_sensors(self,
                                  not_enough_sensors=False):
        _tubes_with_enough_sensors = []
        _connected_sensors = \
            self.connected_sensors(not_enough_sensors=not_enough_sensors)
        for i in range(len(_connected_sensors)):
            if ("SPL06-007" in _connected_sensors[i]
                and "SFM3300" in _connected_sensors[i]):
                _tubes_with_enough_sensors.append(i)
        return _tubes_with_enough_sensors

    def poll_sensors(self):
        """Pulls data from the pressure and flow sensors"""

        # placeholder
        while True:    
            yield tuple((random.uniform(0, 1), random.uniform(0, 1))
                        for _ in range(self._number_of_patients))


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

    sensor_data = poll_sensors(constants.NUMBER_OF_PATIENTS)
    calculator = Calculator(constants.NUMBER_OF_PATIENTS)
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
