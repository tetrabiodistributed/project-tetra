import random
from abc import ABC, abstractmethod

from processsampledata import ProcessSampleData
import constants


class SensorsBase(ABC):

    @abstractmethod
    def __init__(self,
                 pressure_sampling_rate,
                 pressure_oversampling,
                 temperature_sampling_rate,
                 temperature_oversampling):
        super().__init__()

    @abstractmethod
    def calibrate(self):
        pass

    @abstractmethod
    def connected_sensors(self):
        pass

    @abstractmethod
    def calibration_pressure_sensor_connected(self):
        pass

    @abstractmethod
    def tubes_with_enough_sensors(self):
        pass

    @abstractmethod
    def poll_sensors(self):
        pass


def is_on_raspberry_pi():
    """Method to determine if the current platform is a Raspberry Pi.
    It's able to tell Pis from similar boards like Beaglebone Blacks.

    Adapted from https://github.com/adafruit/Adafruit_Python_GPIO/blob/master/Adafruit_GPIO/Platform.py
    """
    try:
        with open('/proc/cpuinfo', 'r') as infile:
            cpuinfo = infile.read()
        # Match a line like 'Hardware   : BCM2709'
        match = re.search('^Hardware\s+:\s+(\w+)$', cpuinfo,
                          flags=re.MULTILINE | re.IGNORECASE)
        if not match:
            # Couldn't find the hardware, assume it isn't a pi.
            return False
        if (match.group(1) == 'BCM2708'  # Pi 1
            or match.group(1) == 'BCM2709'  # Pi 2
            or match.group(1) == 'BCM2835'):  # Pi 3
            return True
        else:
            # Something else, not a pi.
            return False
    except FileNotFoundError:
        return False


if is_on_raspberry_pi():


    class Sensors(SensorsBase):
        """Actual implementation"""
        def __init__(self,
                     pressure_sampling_rate,
                     pressure_oversampling,
                     temperature_sampling_rate,
                     temperature_oversampling):
            pass

        def calibrate(self):
            pass

        def connected_sensors(self):
            pass

        def calibration_pressure_sensor_connected(self):
            pass

        def tubes_with_enough_sensors(self):
            pass

        def poll_sensors(self):
            pass


else:


    class Sensors(SensorsBase):
        """Dummy class while I work on the real thing"""

        def __init__(self,
                     pressure_sampling_rate,
                     pressure_oversampling,
                     temperature_sampling_rate,
                     temperature_oversampling):
            self._fake_data = \
                ProcessSampleData("TestData/20200609T2358Z_patrickData.txt")

        def calibrate(self):
            pass

        def connected_sensors(self, not_enough_sensors=False):
            if not_enough_sensors:
                connected_sensors = \
                    tuple([(constants.PRESSURE_SENSOR,)]
                          + [(constants.PRESSURE_SENSOR,
                              constants.SENSIRION_SENSOR)
                             for _ in range(constants.NUMBER_OF_PATIENTS-1)])
                raise NotEnoughSensors("Tube(s) "
                                       + str([tube
                                              for tube in connected_sensors
                                              if len(tube) < 2])
                                       + "do not have both a pressure "
                                       "and flow sensor")
            else:
                return tuple((constants.PRESSURE_SENSOR,
                              constants.SENSIRION_SENSOR)
                             for _ in range(constants.NUMBER_OF_PATIENTS))

        def calibration_pressure_sensor_connected(self, fail=False):
            if fail:
                return False
            else:
                return True

        def tubes_with_enough_sensors(self,
                                      not_enough_sensors=False):
            tubes_with_enough_sensors = []
            connected_sensors = \
                self.connected_sensors(not_enough_sensors=not_enough_sensors)
            print(connected_sensors[0])
            for i in range(len(connected_sensors)):
                if (constants.PRESSURE_SENSOR in connected_sensors[i]
                    and constants.SENSIRION_SENSOR in connected_sensors[i]):
                    tubes_with_enough_sensors.append(i)
            return tubes_with_enough_sensors

        def poll_sensors(self):
            """Pulls data from the pressure and flow sensors"""

            return next(self._get_next_datum())

        def _get_next_datum(self):
            for i in range(len(self._fake_data)):
                yield tuple((self._fake_data.pressures[i],
                             self._fake_data.flow_rates[i]) for _ in range(4))


class NotEnoughSensors(Exception):
    pass
