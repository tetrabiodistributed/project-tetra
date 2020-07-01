import os
import random
from abc import ABC, abstractmethod

from processsampledata import ProcessSampleData
from rpi_check import is_on_raspberry_pi
import constants


class SensorsDataABC(ABC):

    @abstractmethod
    def __init__(self,
                 pressure_sampling_rate,
                 pressure_oversampling,
                 temperature_sampling_rate,
                 temperature_oversampling):
        super().__init__()

    @abstractmethod
    def connected_sensors(self):
        pass

    @abstractmethod
    def calibration_pressure_sensor_connected(self):
        pass

    @abstractmethod
    def poll(self):
        pass


if is_on_raspberry_pi():

    class SensorsData(SensorsDataABC):
        """Actual implementation"""

        def __init__(self,
                     pressure_sampling_rate,
                     pressure_oversampling,
                     temperature_sampling_rate,
                     temperature_oversampling):
            pass

        def connected_sensors(self):
            pass

        def calibration_pressure_sensor_connected(self):
            pass

        def poll(self):
            pass


else:

    class SensorsData(SensorsDataABC):
        """Dummy class while I work on the real thing"""

        def __init__(self,
                     pressure_sampling_rate,
                     pressure_oversampling,
                     temperature_sampling_rate,
                     temperature_oversampling):
            self._fake_data = \
                ProcessSampleData("TestData/20200609T2358Z_patrickData.txt")
            self._data_index = 0

        def connected_sensors(self, not_enough_sensors=False):
            try:
                if (os.environ[constants.SENSOR_QUANTITY]
                        == constants.NOT_ENOUGH_SENSORS):
                    sensors = tuple([(constants.PRESSURE_SENSOR,)]
                                    + [(constants.PRESSURE_SENSOR,
                                        constants.SENSIRION_SENSOR)
                                       for _ in range(constants.
                                                      NUMBER_OF_PATIENTS-1)
                                       ])
                    raise NotEnoughSensors(
                        f"{len(self._tubes_with_enough_sensors(sensors))} "
                        "tube(s) do not have both a pressure sensor "
                        "and a flow sensor")

                elif (os.environ[constants.SENSOR_QUANTITY]
                      == constants.TOO_MANY_SENSORS):
                    return tuple([(constants.PRESSURE_SENSOR,
                                   constants.SENSIRION_SENSOR,
                                   constants.MASS_AIRFLOW_SENSOR)]
                                 + [(constants.PRESSURE_SENSOR,
                                     constants.SENSIRION_SENSOR)
                                    for _ in range(constants.
                                                   NUMBER_OF_PATIENTS-1)
                                    ])
            except KeyError:
                pass
            return tuple((constants.PRESSURE_SENSOR,
                          constants.SENSIRION_SENSOR)
                         for _ in range(constants.NUMBER_OF_PATIENTS))

        def calibration_pressure_sensor_connected(self, fail=False):
            if fail:
                return False
            else:
                return True

        def poll(self):
            """Pulls data from the pressure and flow sensors"""
            self._data_index += 1
            return tuple((self._fake_data.pressures[self._data_index-1],
                          self._fake_data.flow_rates[self._data_index-1])
                         for _ in range(constants.NUMBER_OF_PATIENTS))

        def _tubes_with_enough_sensors(self, tubes_sensors):
            tubes = []
            for tube in tubes_sensors:
                if (constants.PRESSURE_SENSOR in tube
                    and (constants.SENSIRION_SENSOR in tube
                         or constants.MASS_AIRFLOW_SENSOR in tube)):
                    tubes.append(tube)
            return tubes


class Sensors():

    def __init__(self,
                 pressure_sampling_rate,
                 pressure_oversampling,
                 temperature_sampling_rate,
                 temperature_oversampling):
        self._sensors_data = SensorsData(pressure_sampling_rate,
                                         pressure_oversampling,
                                         temperature_sampling_rate,
                                         temperature_oversampling)

    def calibrate(self):
        pass

    def calibration_pressure_sensor_connected(self):
        pass

    def tubes_with_enough_sensors(self):
        tubes = []
        sensors = self._sensors_data.connected_sensors()
        for i in range(len(sensors)):
            if (constants.PRESSURE_SENSOR in sensors[i]
                and (constants.SENSIRION_SENSOR in sensors[i])
                    or constants.MASS_AIRFLOW_SENSOR in sensors[i]):
                tubes.append(i)

        return tubes

    def poll(self):
        return self._sensors_data.poll()


class NotEnoughSensors(Exception):
    pass
