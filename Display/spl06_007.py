import time
import sys
import warnings
import math

import board
import busio


class PressureSensor():

    def __init__(self):
        self._communicator = I2CCommunication()
        self._sampling_set = False
        self._first_measurement_has_happened = False

    def close(self):
        self._communicator.close()

    def set_sampling(self,
                     pressure_oversample=16,
                     pressure_sampling_rate=1,
                     temperature_oversample=1,
                     temperature_sampling_rate=1):
        self._communicator.set_pressure_sampling(oversample=pressure_oversample,
                                                 rate=pressure_sampling_rate)
        self._communicator.set_temperature_sampling(
            oversample=temperature_oversample,
            rate=temperature_sampling_rate
        )
        
        self._calibrator = Calibrator(
            self._communicator.calibration_coefficients,
            self._communicator.pressure_scale_factor,
            self._communicator.temperature_scale_factor
        )

        self._sampling_set = True
        return self._sampling_set
        
    def set_op_mode(self, op_mode):
        return self._communicator.set_op_mode(op_mode)

    def pressure(self):
        if self._sampling_set:
            self._first_measurement_delay()
            return self._calibrator.pressure(
                self._communicator.raw_pressure(),
                self._communicator.raw_temperature()
            )
        else:
            return float("nan")

    def temperature(self):
        if self._sampling_set:
            self._first_measurement_delay()
            return self._calibrator.temperature(
                self._communicator.raw_temperature()
            )
        else:
            return float("nan")

            # """Default mode after power on or reset. No measurements
        # are performed.  All registers and compensation coefficients
        # are accessible"""

                # """One temperature or pressure measurement is performed
        # according to the selected precision.  The sensor will
        # return to Standby Mode when the measurement is finished, and
        # the measurement result will be available in the data registers.
        # """

        # """Pressure and/or temperature measurements are performed
        # continuously according to the selected measurement precision
        # and rate. The temperature measurement is performed immediately
        # after the pressure measurement.
        # The FIFO can be used to store 32 measurement results and minimize
        # the number of times the sensor must be accessed to read out the
        # results"""
    
    class OpMode():
        standby = "Standby"
        background = "Background"
        command = "Command"

    def _first_measurement_delay(self):
        first_measurement_delay = 0.151
        if self._first_measurement_has_happened:
            self._first_measurement_has_happened = True
            time.sleep(first_measurement_delay)


class Calibrator():

    def __init__(self,
                 calibration_coefficients,
                 pressure_scaling_factor,
                 temperature_scaling_factor):
        self._c0 = calibration_coefficients[0]
        self._c1 = calibration_coefficients[1]
        self._c00 = calibration_coefficients[2]
        self._c10 = calibration_coefficients[3]
        self._c01 = calibration_coefficients[4]
        self._c11 = calibration_coefficients[5]
        self._c20 = calibration_coefficients[6]
        self._c21 = calibration_coefficients[7]
        self._c30 = calibration_coefficients[8]

        if (math.isclose(pressure_scaling_factor, 0.0)
            or math.isclose(temperature_scaling_factor, 0.0)):
            raise ZeroDivisionError("Cannot have pressure or temperature "
                                    "scaling factor equal to 0.")

        self._pressure_scaling_factor = pressure_scaling_factor
        self._temperature_scaling_factor = temperature_scaling_factor

    def pressure(self, raw_pressure, raw_temperature):
        scaled_pressure = raw_pressure / self._pressure_scaling_factor
        scaled_temperature = raw_temperature / self._temperature_scaling_factor

        compensated_pressure = (                                       
            self._c00
            + scaled_pressure*(self._c10
                               + scaled_pressure*(self._c20
                                                  + scaled_pressure*self._c30))
            + scaled_temperature*self._c01
            + scaled_temperature*scaled_pressure*(self._c11
                                                  + scaled_pressure*self._c21)
        )                                                              
        return compensated_pressure

    def temperature(self, raw_temperature):
        scaled_temperature = raw_temperature / self._temperature_scaling_factor
        compensated_temperature = self._c0 * 0.5 + self._c1 * scaled_temperature
        return compensated_temperature


class I2CCommunication():
    """Performs I2C communication between a Raspberry Pi and a
    SPL06-007 pressure sensor.

    Parameters
    ----------
    SDO_high=True: bool
        Set to false if the SDO pin on the SPL06-007 is pulled to ground
    """

    _DEVICE_ADDRESS_SDO_HIGH = 0x77
    _DEVICE_ADDRESS_SDO_LOW = 0x76
        
    # Register addresses
    _PRESSURE_MSB  = 0x00
    _PRESSURE_LSB  = 0x01
    _PRESSURE_XLSB = 0x02
    _TEMPERATURE_MSB  = 0x03
    _TEMPERATURE_LSB  = 0x04
    _TEMPERATURE_XLSB = 0x05
    _PRESSURE_CONFIGURATION = 0x06
    _TEMPERATURE_CONFIGURATION = 0x07
    _SENSOR_OP_MODE = 0x08
    _INTERRUPT_AND_FIFO_CONFIGURATION = 0x09
    _INTERRUPT_STATUS = 0x0A
    _FIFO_STATUS = 0x0B
    _RESET_AND_FLUSH = 0x0C
    _PRODUCT_AND_REVISION_ID = 0x0D
    # Calibration Coefficient register addresses
    _C0_11_4        = 0x10
    _C0_3_0_C1_11_8 = 0x11
    _C1_7_0         = 0x12
    _C00_19_12         = 0x13
    _C00_11_4          = 0x14
    _C00_3_0_C10_19_16 = 0x15
    _C10_15_8          = 0x16
    _C10_7_0           = 0x17
    _C01_15_8          = 0x18
    _C01_7_0           = 0x19
    _C11_15_8          = 0x1A
    _C11_7_0           = 0x1B
    _C20_15_8          = 0x1C
    _C20_7_0           = 0x1D
    _C21_15_8          = 0x1E
    _C21_7_0           = 0x1F
    _C30_15_8          = 0x20
    _C30_7_0           = 0x21

    # Bitmasks to read from registers
    #   Read these from self._SENSOR_OP_MODE
    _COEF_RDY   = 0b10000000
    _SENSOR_RDY = 0b01000000
    _TMP_RDY    = 0b00100000
    _PRS_RDY    = 0b00010000
    #   Read these from self._INTERRUPT_STATUS
    _INT_FIFO_FULL = 0b00000100
    _INT_TMP       = 0b00000010
    _INT_PRS       = 0b00000001
    #   Read these from self._FIFO_STATUS
    _FIFO_FULL  = 0b00000010
    _FIFO_EMPTY = 0b00000001
    #   Read these from self._PRODUCT_AND_REVISION_ID
    _PROD_ID = 0b11110000
    _REV_ID  = 0b00001111
    
    # Codes to write to registers
    #   Write these to self._PRESSURE_CONFIGURATION
    #   The rate and oversample can bitwise-or'ed together
    _PRESSURE_RATE_1HZ   = 0b00000000
    _PRESSURE_RATE_2HZ   = 0b00010000
    _PRESSURE_RATE_4HZ   = 0b00100000
    _PRESSURE_RATE_8HZ   = 0b00110000
    _PRESSURE_RATE_16HZ  = 0b01000000
    _PRESSURE_RATE_32HZ  = 0b01010000
    _PRESSURE_RATE_64HZ  = 0b01100000
    _PRESSURE_RATE_128HZ = 0b01110000
    _PRESSURE_OVERSAMPLE_1X   = 0b00000000
    _PRESSURE_OVERSAMPLE_2X   = 0b00000001
    _PRESSURE_OVERSAMPLE_4X   = 0b00000010
    _PRESSURE_OVERSAMPLE_8X   = 0b00000011
    _PRESSURE_OVERSAMPLE_16X  = 0b00000100
    _PRESSURE_OVERSAMPLE_32X  = 0b00000101
    _PRESSURE_OVERSAMPLE_64X  = 0b00000110
    _PRESSURE_OVERSAMPLE_128X = 0b00000111
    #   Write these to self._TEMPERATURE_CONFIGURATION
    #   The sensor, rate, and can be bitwise-or'ed together
    _TEMPERATURE_SENSOR_INTERNAL = 0b10000000
    _TEMPERATURE_SENSOR_EXTERNAL = 0b00000000
    _TEMPERATURE_RATE_1HZ   = 0b00000000
    _TEMPERATURE_RATE_2HZ   = 0b00010000
    _TEMPERATURE_RATE_4HZ   = 0b00100000
    _TEMPERATURE_RATE_8HZ   = 0b00110000
    _TEMPERATURE_RATE_16HZ  = 0b01000000
    _TEMPERATURE_RATE_32HZ  = 0b01010000
    _TEMPERATURE_RATE_64HZ  = 0b01100000
    _TEMPERATURE_RATE_128HZ = 0b01110000
    _TEMPERATURE_OVERSAMPLE_1X   = 0b00000000
    _TEMPERATURE_OVERSAMPLE_2X   = 0b00000001
    _TEMPERATURE_OVERSAMPLE_4X   = 0b00000010
    _TEMPERATURE_OVERSAMPLE_8X   = 0b00000011
    _TEMPERATURE_OVERSAMPLE_16X  = 0b00000100
    _TEMPERATURE_OVERSAMPLE_32X  = 0b00000101
    _TEMPERATURE_OVERSAMPLE_64X  = 0b00000110
    _TEMPERATURE_OVERSAMPLE_128X = 0b00000111
    #   Write these to self._SENSOR_OP_MODE
    _STANDBY                         = 0b00000000
    _COMMAND_PRESSURE                = 0b00000001
    _COMMAND_TEMPERATURE             = 0b00000010
    _BACKGROUND_PRESSURE             = 0b00000101
    _BACKGROUND_TEMPERATURE          = 0b00000110
    _BACKGROUND_PRESSURE_TEMPERATURE = 0b00000111
    #  Read or write these to self._INTERRUPT_AND_FIFO_CONFIGURATION
    #  Note: temperature or pressure bit shift must be set when
    #  their respective oversample rates are set to > 8
    _SET_INTERRUPT_ACTIVE_LEVEL                   = 0b10000000
    _GENERATE_INTERRUPT_WHEN_FIFO_IS_FULL         = 0b01000000
    _GENERATE_INTERRUPT_WHEN_PRESSURE_IS_READY    = 0b00100000
    _GENERATE_INTERRUPT_WHEN_TEMPERATURE_IS_READY = 0b00010000
    _TEMPERATURE_RESULT_BIT_SHIFT                 = 0b00001000
    _PRESSURE_RESULT_BIT_SHIFT                    = 0b00000100
    _ENABLE_FIFO                                  = 0b00000010
    _SET_4_WIRE_SPI                               = 0b00000000
    _SET_3_WIRE_SPI                               = 0b00000001
    #   Write these to self._RESET_AND_FLUSH
    #   They can be bitwise-or'ed together
    _FLUSH_FIFO = 0b10000000
    _SOFT_RESET = 0b00001001

    # For use in calibrating the sensor, taken from Table 4 of
    # the data sheet
    _COMPENSATION_SCALE_FACTORS = {1: 524288,
                                   2: 1572864,
                                   4: 3670016,
                                   8: 7864320,
                                   16: 253952,
                                   32: 516096,
                                   64: 1040384,
                                   128: 2088960}

    # Some helper constants
    _PRESSURE_RATE_OPTIONS = {1: _PRESSURE_RATE_1HZ,
                              2: _PRESSURE_RATE_2HZ,
                              4: _PRESSURE_RATE_4HZ,
                              8: _PRESSURE_RATE_8HZ,
                              16: _PRESSURE_RATE_16HZ,
                              32: _PRESSURE_RATE_32HZ,
                              64: _PRESSURE_RATE_64HZ,
                              128: _PRESSURE_RATE_128HZ}
    _PRESSURE_OVERSAMPLE_OPTIONS = {1: _PRESSURE_OVERSAMPLE_1X,
                                    2: _PRESSURE_OVERSAMPLE_2X,
                                    4: _PRESSURE_OVERSAMPLE_4X,
                                    8: _PRESSURE_OVERSAMPLE_8X,
                                    16: _PRESSURE_OVERSAMPLE_16X,
                                    32: _PRESSURE_OVERSAMPLE_32X,
                                    64: _PRESSURE_OVERSAMPLE_64X,
                                    128: _PRESSURE_OVERSAMPLE_128X}
    _TEMPERATURE_RATE_OPTIONS = {1: _TEMPERATURE_RATE_1HZ, 
                                 2: _TEMPERATURE_RATE_2HZ, 
                                 4: _TEMPERATURE_RATE_4HZ, 
                                 8: _TEMPERATURE_RATE_8HZ, 
                                 16: _TEMPERATURE_RATE_16HZ,
                                 32: _TEMPERATURE_RATE_32HZ,
                                 64: _TEMPERATURE_RATE_64HZ,
                                 128: _TEMPERATURE_RATE_128HZ}
    _TEMPERATURE_OVERSAMPLE_OPTIONS = {1: _TEMPERATURE_OVERSAMPLE_1X,
                                       2: _TEMPERATURE_OVERSAMPLE_2X,
                                       4: _TEMPERATURE_OVERSAMPLE_4X,
                                       8: _TEMPERATURE_OVERSAMPLE_8X,
                                       16: _TEMPERATURE_OVERSAMPLE_16X,
                                       32: _TEMPERATURE_OVERSAMPLE_32X,
                                       64: _TEMPERATURE_OVERSAMPLE_64X,
                                       128: _TEMPERATURE_OVERSAMPLE_128X}

    _READY_WAIT_TIME = 0.0036

    def __init__(self, SDO_high=True):
        """The sensor takes (107 +/- 8) ms to initialize."""
        if SDO_high:
            self._i2c_address = self._DEVICE_ADDRESS_SDO_HIGH
        else:
            self._i2c_address = self._DEVICE_ADDRESS_SDO_LOW
        self._i2c = busio.I2C(board.SCL, board.SDA)
        while not self._i2c.try_lock():
            pass
        self._find_sensor()
        self._reset_sensor()
        self.set_op_mode(PressureSensor.OpMode.standby)
        self._calculate_calibration_coefficients()

    def close(self):
        self._i2c.unlock()
        self._i2c.deinit()
        self._i2c.deinit()

    @property
    def mode_standby(self):
        # """Default mode after power on or reset. No measurements
        # are performed.  All registers and compensation coefficients
        # are accessible"""
        return 0

    @property
    def mode_command(self):
        # """One temperature or pressure measurement is performed
        # according to the selected precision.  The sensor will
        # return to Standby Mode when the measurement is finished, and
        # the measurement result will be available in the data registers.
        # """
        return 1

    @property
    def mode_background(self):
        # """Pressure and/or temperature measurements are performed
        # continuously according to the selected measurement precision
        # and rate. The temperature measurement is performed immediately
        # after the pressure measurement.
        # The FIFO can be used to store 32 measurement results and minimize
        # the number of times the sensor must be accessed to read out the
        # results"""
        return 2

    def set_op_mode(self, mode):
        """Sets the pressure sensor into a mode for data collection
        
        Parameters
        ----------
        mode : {PressureSensor.OpMode.standby,
                PressureSensor.OpMode.command,
                PressureSensor.OpMode.background}
            The data output modes of the sensor
        use_pressure=True : bool
            Set to False if you don't want pressure data; it's
            otherwise True
        use_temperature=True : bool
            Set to False if you don't want temperature data;
            it's otherwise True
        """

        set_standby = False
        if mode == PressureSensor.OpMode.command:
            self._op_mode = PressureSensor.OpMode.command
            return PressureSensor.OpMode.command
        
        elif mode == PressureSensor.OpMode.background:
            self._write_register(self._SENSOR_OP_MODE,
                                 self._BACKGROUND_PRESSURE_TEMPERATURE)
            self._op_mode = PressureSensor.OpMode.background
            return PressureSensor.OpMode.background
        
        else:
            if mode != PressureSensor.OpMode.standby:
                warnings.warn("Undefined mode.  Defaulting to"
                              "Standby Mode",
                              RuntimeWarning)
            set_standby = True
        if set_standby:
            self._write_register(self._SENSOR_OP_MODE, self._STANDBY)
            self._op_mode = PressureSensor.OpMode.standby
            return PressureSensor.OpMode.standby

    @property
    def calibration_coefficients(self):

        return self._calibration_coefficients

    def set_pressure_sampling(self, oversample=16, rate=1):
        """Set the amount of oversampling and the sampling rate

        Parameters
        ----------
        oversample=16 : {1, 2, 4, 8, 16, 32, 64, 128}
            The SPL06-007 reads the sensor multiple times and combines
            them into one result to achieve a higher precision. This
            increases the current consumption and the measurement time,
            which again reduces the maximum measurement rate.
            The measurement times and precision for each oversample are
            these values.
            | Oversampling | Measurement time [ms] | Precision [Pa RMS] |
            |--------------|-----------------------|--------------------|
            |            1 |                   3.6 |                  5 |
            |            2 |                   5.2 |                    |
            |            4 |                   8.4 |                2.5 |
            |            8 |                  14.8 |                    |
            |           16 |                  27.6 |                1.2 |
            |           32 |                  53.2 |                0.9 |
            |           64 |                 104.4 |                0.5 |
            |          128 |                 206.8 |                    |
        rate=1 : {1, 2, 4, 8, 16, 32, 64, 128}
            The sampling rate of the sensor in hertz.  The sampling rate
            is only relevant in Background Mode.
        """

        try:
            rate_mode = self._PRESSURE_RATE_OPTIONS[rate]
        except KeyError:
            raise ValueError("Pressure sampling rate can only be "
                             "1, 2, 4, 8, 16, 32, 64, or 128 Hz")
        try:
            oversample_mode = self._PRESSURE_OVERSAMPLE_OPTIONS[oversample]
            self._pressure_scale_factor = \
                self._COMPENSATION_SCALE_FACTORS[oversample]
        except KeyError:
            raise ValueError("Pressure oversampling can only be "
                             "1, 2, 4, 8, 16, 32, 64, or 128X")
        self._write_register(self._PRESSURE_CONFIGURATION,
                             rate_mode | oversample_mode)
        if oversample > 8:
            self._write_register(self._INTERRUPT_AND_FIFO_CONFIGURATION,
                                 self._PRESSURE_RESULT_BIT_SHIFT)
        else:
            new_interrupt_and_fifo_configuration_state = (
                self._read_register(self._INTERRUPT_AND_FIFO_CONFIGURATION)
                ) & (0xff - self._PRESSURE_RESULT_BIT_SHIFT)
            self._write_register(self._INTERRUPT_AND_FIFO_CONFIGURATION,
                                 new_interrupt_and_fifo_configuration_state)

    def raw_pressure(self):
        """The raw pressuring reading from the sensor.  This needs to
        be scaled and compensated to be useful.
        """
        if self._op_mode == PressureSensor.OpMode.command:
            self._write_register(self._SENSOR_OP_MODE, self._COMMAND_PRESSURE)
            
        while (self._read_register(self._SENSOR_OP_MODE) & self._PRS_RDY) == 0:
            time.sleep(self._READY_WAIT_TIME)
        pressure_msb = self._read_register(self._PRESSURE_MSB)
        pressure_lsb = self._read_register(self._PRESSURE_LSB)
        pressure_xlsb = self._read_register(self._PRESSURE_XLSB)
        pressure = self._twos_complement(((pressure_msb << 16)
                                          + (pressure_lsb << 8)
                                          + pressure_xlsb),
                                         24)
        return pressure

    @property
    def pressure_scale_factor(self):
        """A constant used for calibrating the sensor"""
        
        return self._pressure_scale_factor

    def set_temperature_sampling(self, oversample=1, rate=1):
        """Set the amount of oversampling and the sampling rate

        Parameters
        ----------
        oversample=1 : {1, 2, 4, 8, 16, 32, 64, 128}
            The SPL06-007 reads the sensor multiple times and combines
            them into one result to achieve a higher precision. This
            increases the current consumption and the measurement time,
            which again reduces the maximum measurement rate.
            Setting the oversample for temperature is optional and may
            not be relevant.
            The measurement time for oversample=1 is 3.6 ms.
        rate=1 : {1, 2, 4, 8, 16, 32, 64, 128}
            The sampling rate of the sensor in hertz.  The sampling rate
            is only relevant in background mode.
        """
                                                          
        try:                                              
            rate_mode = self._TEMPERATURE_RATE_OPTIONS[rate] 
        except KeyError:                                  
            raise ValueError("Temperature sampling rate can only be "
                             "1, 2, 4, 8, 16, 32, 64, or 128 Hz")
        try:                                              
            oversample_mode = self._TEMPERATURE_OVERSAMPLE_OPTIONS[oversample]
            self._temperature_scale_factor = \
                self._COMPENSATION_SCALE_FACTORS[oversample]
        except KeyError:                                  
            raise ValueError("Temperature oversampling can only be "
                             "1, 2, 4, 8, 16, 32, 64, or 128X")
        self._write_register(self._TEMPERATURE_CONFIGURATION,
                             rate_mode | oversample_mode)
        if oversample > 8:
            self._write_register(self._INTERRUPT_AND_FIFO_CONFIGURATION,
                                 self._TEMPERATURE_RESULT_BIT_SHIFT)
        else:
            new_interrupt_and_fifo_configuration_state = (
                self._read_register(self._INTERRUPT_AND_FIFO_CONFIGURATION)
                ) & (0xff - self._TEMPERATURE_RESULT_BIT_SHIFT)
            self._write_register(self._INTERRUPT_AND_FIFO_CONFIGURATION,
                                 new_interrupt_and_fifo_configuration_state)

    def raw_temperature(self):
        """The raw temperature reading from the sensor.  This need to
        be scaled and compensated to be useful.
        """
        if self._op_mode == PressureSensor.OpMode.command:
            self._write_register(self._SENSOR_OP_MODE,
                                 self._COMMAND_TEMPERATURE)
        
        while (self._read_register(self._SENSOR_OP_MODE) & self._TMP_RDY) == 0:
            time.sleep(self._READY_WAIT_TIME)
        temperature_msb = self._read_register(self._TEMPERATURE_MSB) << 16
        temperature_lsb = self._read_register(self._TEMPERATURE_LSB) << 8
        temperature_xlsb = self._read_register(self._TEMPERATURE_XLSB)
        temperature = self._twos_complement((temperature_msb    
                                             + temperature_lsb  
                                             + temperature_xlsb),
                                            24)
        return temperature

    @property
    def temperature_scale_factor(self):
        """A constant used for calibrating the sensor."""

        return self._temperature_scale_factor
        

    def _calculate_calibration_coefficients(self):
        """The SPL06-007 is a calibrated sensor and contains
        calibration coefficients. These are used in the
        application (for instance by the host processor) to
        compensate the measurement results for sensor nonlinearity’s.

        Note: The coefficients read from the coefficient register
        {c00, c10, c01, c11, c20, c21, c30} are 16 bit 2´s complement
        numbers.

        Note: The coefficients read from the coefficient register
        {c0, c1} 12 bit 2´s complement numbers.
        """

        while (self._read_register(self._SENSOR_OP_MODE) & self._COEF_RDY) == 0:
            time.sleep(self._READY_WAIT_TIME)

        _c0_11_4 =           self._read_register(self._C0_11_4)
        _c0_3_0_c1_11_8 =    self._read_register(self._C0_3_0_C1_11_8)
        _c1_7_0 =            self._read_register(self._C1_7_0)
        _c00_19_12 =         self._read_register(self._C00_19_12)
        _c00_11_4 =          self._read_register(self._C00_11_4)
        _c00_3_0_c10_19_16 = self._read_register(self._C00_3_0_C10_19_16)
        _c10_15_8 =          self._read_register(self._C10_15_8)
        _c10_7_0 =           self._read_register(self._C10_7_0)
        _c01_15_8 =          self._read_register(self._C01_15_8)
        _c01_7_0 =           self._read_register(self._C01_7_0)
        _c11_15_8 =          self._read_register(self._C11_15_8)
        _c11_7_0 =           self._read_register(self._C11_7_0)
        _c20_15_8 =          self._read_register(self._C20_15_8)
        _c20_7_0 =           self._read_register(self._C20_7_0)
        _c21_15_8 =          self._read_register(self._C21_15_8)
        _c21_7_0 =           self._read_register(self._C21_7_0)
        _c30_15_8 =          self._read_register(self._C30_15_8)
        _c30_7_0 =           self._read_register(self._C30_7_0)

        most_significant_nibble = lambda byte : (byte & 0xf0) >> 4
        least_significant_nibble = lambda byte : byte & 0x0f

        c0 = self._twos_complement(
            (_c0_11_4 << 4) | most_significant_nibble(_c0_3_0_c1_11_8),
            12
        )
        c1 = self._twos_complement(
            (least_significant_nibble(_c0_3_0_c1_11_8) << 8) | _c1_7_0,
            12
        )
        
        c00 = self._twos_complement(
            (_c00_19_12 << 12) | (_c00_11_4 << 4)
            | most_significant_nibble(_c00_3_0_c10_19_16),
            16
        )
        c10 = self._twos_complement(
            (least_significant_nibble(_c00_3_0_c10_19_16) << 16)
            | (_c10_15_8 << 8) | _c10_7_0,
            16
        )
        c01 = self._twos_complement((_c01_15_8 << 8) | _c01_7_0, 16)
        c11 = self._twos_complement((_c11_15_8 << 8) | _c11_7_0, 16)
        c20 = self._twos_complement((_c20_15_8 << 8) | _c20_7_0, 16)
        c21 = self._twos_complement((_c21_15_8 << 8) | _c21_7_0, 16)
        c30 = self._twos_complement((_c30_15_8 << 8) | _c30_7_0, 16)
        
        self._calibration_coefficients = (c0, c1,
                                          c00, c10, c01, c11, c20, c21, c30)

    def _find_sensor(self):
        while not self._i2c_address in self._i2c.scan():
            time.sleep(self._READY_WAIT_TIME)

    def _reset_sensor(self):
        reset_time = 0.02
        self._write_register(self._RESET_AND_FLUSH, self._SOFT_RESET)
        time.sleep(reset_time)
        while (self._read_register(self._SENSOR_OP_MODE)
               & self._SENSOR_RDY == 0):
            # Wait for the sensor to be ready
            time.sleep(0.005)

    def _read_register(self, register):
        data = bytearray(1)
        self._i2c.writeto(self._i2c_address, bytes([register]))
        print(f"{1000*time.time():.4f} TX -> {bytes([register]).hex()}")
        self._i2c.readfrom_into(self._i2c_address, data)
        print(f"{1000*time.time():.4f} RX <- {data.hex()}")
        return int(data.hex(), 16)

    def _write_register(self, register, to_write):
        self._i2c.writeto(self._i2c_address, bytes([register, to_write]))
        print(f"{1000*time.time():.4f} TX -> {bytes([register, to_write]).hex()}")
                
    def _twos_complement(self, value, bits):
        
        if (value & (1 << (bits - 1))) != 0:
            complement = (value & (2**bits - 1)) - (1 << bits)
        else:
            complement = value & (2**bits - 1)
        return complement


# class SPICommunication():

#     def __init__(self, four_pin=True):
#         """The sensor takes (107 +/- 8) ms to initialize."""
#         self._i2c = busio.SPI(
#         if not four_pin::
#             pass
#         while not self._i2c.try_lock():
#             pass
#         self._find_sensor()
#         self._reset_sensor()
#         self.set_op_mode(PressureSensor.OpMode.standby)
#         self._calculate_calibration_coefficients()
        

if "__main__" == __name__:
    print("--Initialization")
    comms = I2CCommunication()
    print("--Set Op Mode")
    comms.set_op_mode(PressureSensor.OpMode.command)
    print("--Set Pressure Sampling")
    comms.set_pressure_sampling()
    print("--Set Temperature Sampling")
    comms.set_temperature_sampling()
    # print(comms.calibration_coefficients)
    calibrator = Calibrator(comms.calibration_coefficients,
                            comms.pressure_scale_factor,
                            comms.temperature_scale_factor)
    #time.sleep(0.151)
    running = True
    while running:
        try:
            print("--Get Pressure")
            raw_pressure = comms.raw_pressure()
            print("--Get Temperature")
            raw_temperature = comms.raw_temperature()
            pressure = calibrator.pressure(raw_pressure, raw_temperature)
            temperature = calibrator.temperature(raw_temperature)
            # print(f"pressure: {pressure}\ttemperature: {temperature}\n"
            #       f"raw pressure: {raw_pressure}\t\t"
            #       f"raw temperature: {raw_temperature}\n")
            time.sleep(1.0)
            break
        except KeyboardInterrupt:
            running = False
            comms.close()
