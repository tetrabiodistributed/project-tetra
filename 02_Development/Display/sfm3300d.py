import time
import math

import crcmod

from i2c_interface import I2CInterface


class FlowSensor():
    """An interface for initizlizing and getting calibrated data from a
    SFM3300-D flow sensor.  The data sheet for the sensor can be found at
    https://www.mouser.com/datasheet/2/682/Sensirion_Mass_Flow_Meters_SFM3300_Datasheet-1524535.pdf
    """

    def __init__(self, dump_communication=False):
        """Initializes self."""
        self._calibrator = Calibrator(SensorConstants.OFFSET_FLOW,
                                      SensorConstants.SCALE_FACTOR_FLOW)
        self._communicator = Communicator(
            dump_communication=dump_communication)
        self._communicator.init_flow()

    def close(self):
        """Deinitializes the I2C and unlocks the I2C bus."""
        if self.is_present():
            self._communicator.close()

    def is_present(self):
        return self._communicator.is_present()

    def flow(self):
        """Flow rate in standard liters per minute (SFM)."""
        raw_flow = self._communicator.raw_flow()
        if raw_flow >= 0:
            return self._calibrator.flow(self._communicator.raw_flow())
        else:
            return float("nan")

    def serial_number(self):
        """Serial number of the particular sensor being used."""
        return self._communicator.serial_number()


class Calibrator():
    """Takes raw data from a SFM3300-D flow sensor and converts it
    to flow rate in standard liters per minute (SFM).
    """

    def __init__(self, offset_flow=None, scale_factor_flow=None):
        if offset_flow is not None:
            self._offset_flow = offset_flow
        else:
            self._offset_flow = SensorConstants.OFFSET_FLOW

        if scale_factor_flow is not None:
            self._scale_factor_flow = scale_factor_flow
        else:
            self._scale_factor_flow = SensorConstants.SCALE_FACTOR_FLOW
        if math.isclose(self._scale_factor_flow, 0.0):
            raise ZeroDivisionError("scale_factor_flow cannot be zero.")

    def flow(self, measured_value):
        """Flow rate in standard liters per minute (SFM).

        Parameters
        ----------
        measured_value : int
            Raw flow from the sensor.
        """
        return (measured_value - self._offset_flow) / self._scale_factor_flow


class Communicator():
    """Performs I2C communication between a Raspberry Pi and a SFM3300-D
    flow sensor.  The data sheet describing the I2C communication can be
    found at
    https://www.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/5_Mass_Flow_Meters/Application_Notes/Sensirion_Mass_Flo_Meters_SFM3xxx_I2C_Functional_Description.pdf

    And the data sheet the describes the CRC validation used can be found
    at
    https://www.mouser.jp/pdfDocs/SFM3000_CRC_Checksum_Calculation.pdf
    """

    def __init__(self, dump_communication=False):
        """Initializes self."""
        self._i2c = I2CInterface(SensorConstants.ADDRESS,
                                 dump_communication=dump_communication)
        if SensorConstants.ADDRESS in self._i2c.scan():
            print("reset")
            self._reset()
            self._sensor_available = True
        else:
            self._sensor_available = False
        self._flow_inited = False
        self._crc8 = crcmod.mkCrcFun(SensorConstants.CRC_POLYNOMIAL,
                                     initCrc=0x00,
                                     rev=False,
                                     xorOut=0x00)

    def close(self):
        """Deinitializes I2C and unlocks the I2C bus."""
        if self.is_present():
            # self._reset()
            print("present")
        self._i2c.close()

    def is_present(self):
        return self._sensor_available

    def serial_number(self):
        """The serial number of the particular sensor being used."""
        if self.is_present():
            serial_number_bytes = (
                self._i2c.read_register(SensorConstants.READ_SERIAL_NUMBER,
                                        SensorConstants.SERIAL_NUMBER_BYTES))
            serial_number = 0
            for i in range(SensorConstants.SERIAL_NUMBER_BYTES):
                serial_number |= (
                    serial_number_bytes[SensorConstants.SERIAL_NUMBER_BYTES
                                        - i - 1]
                    << (8*i))
            return serial_number
        else:
            return -1

    def init_flow(self):
        """Prepares the sensor to begin reading out data.  It takes about
        100ms to initialize.
        """
        if self.is_present() and not self._flow_inited:
            self._i2c.write_data(SensorConstants.START_CONTINUOUS_MEASUREMENT)
            self._flow_inited = True
            time.sleep(0.100)  # give the sensor a moment to initialize
            self.raw_flow()  # the first datum is garbage

    def raw_flow(self):
        """The raw, uncalibrated flow data."""
        if self.is_present() and self._flow_inited:
            flow_bytes = (
                self._i2c.read_data(SensorConstants.MEASUREMENT_BYTES))
            flow_measurement = bytearray(flow_bytes[0:2])
            if self._crc8(flow_measurement) != flow_bytes[2]:
                raise CRCError("Data fails CRC8 validation.")
            else:
                return int(flow_measurement.hex(), 16)
        else:
            return -1

    def _reset(self):
        self._i2c.write_data(SensorConstants.SOFT_RESET)


class CRCError(Exception):
    pass


class SensorConstants():
    """The names and addresses of every register on the chip and codes
    to write to them.
    """
    ADDRESS = 0x40
    SOFT_RESET = 0x2000
    READ_SERIAL_NUMBER = 0x31AE
    SERIAL_NUMBER_BYTES = 4
    START_CONTINUOUS_MEASUREMENT = 0x1000
    MEASUREMENT_BYTES = 3
    CRC_POLYNOMIAL = 0x131  # x^8 + x^5 + x^4 + 1
    SCALE_FACTOR_FLOW = 120
    OFFSET_FLOW = 32768
