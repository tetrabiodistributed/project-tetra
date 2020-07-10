import time
import math

import crcmod

from i2c_interface import I2CInterface


class FlowSensor():
    """A class!!
    Main Datasheet:
    https://www.mouser.com/datasheet/2/682/Sensirion_Mass_Flow_Meters_SFM3300_Datasheet-1524535.pdf
    """

    def __init__(self):
        self._calibrator = Calibrator(SensorConstants.OFFSET_FLOW,
                                      SensorConstants.SCALE_FACTOR_FLOW)
        self._communicator = Communicator()

    def close(self):
        self._communicator.close()

    def init_flow(self):
        self._communicator.init_flow()
        self._communicator.raw_flow()  # the first datum is garbage

    def flow(self):
        return self._calibrator.flow(self._communicator.raw_flow())

    def serial_number(self):
        return self._communicator.serial_number()


class Calibrator():

    def __init__(self, offset_flow, scale_factor_flow):
        if math.isclose(scale_factor_flow, 0.0):
            raise ZeroDivisionError("scale_factor_flow cannot be zero.")
        self._offset_flow = offset_flow
        self._scale_factor_flow = scale_factor_flow

    def flow(self, measured_value):
        return (measured_value - self._offset_flow) / self._scale_factor_flow


class Communicator():
    """A class!

    I2C Datasheet:
    https://www.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/5_Mass_Flow_Meters/Application_Notes/Sensirion_Mass_Flo_Meters_SFM3xxx_I2C_Functional_Description.pdf

    CRC Note:
    https://www.mouser.jp/pdfDocs/SFM3000_CRC_Checksum_Calculation.pdf"""

    def __init__(self):
        self._i2c = I2CInterface(SensorConstants.ADDRESS)
        self._flow_inited = False
        self._crc8 = crcmod.mkCrcFun(SensorConstants.CRC_POLYNOMIAL,
                                     initCrc=0x00,
                                     rev=False,
                                     xorOut=0x00)

    def close(self):
        self._i2c.close()

    def serial_number(self):
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

    def init_flow(self):
        self._i2c.write_data(SensorConstants.START_CONTINUOUS_MEASUREMENT)
        self._flow_inited = True

    def raw_flow(self):
        if self._flow_inited:
            flow_bytes = (
                self._i2c.read_data(SensorConstants.MEASUREMENT_BYTES))
            flow_measurement = bytearray(flow_bytes[0:2])
            if self._crc8(flow_measurement) != flow_bytes[2]:
                raise CRCError("Data fails CRC8 validation.")
            else:
                return int(flow_measurement.hex(), 16)

        return -1


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
