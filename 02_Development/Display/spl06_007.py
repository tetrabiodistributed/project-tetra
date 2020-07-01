import time
import warnings
import math

from i2c_interface import I2CInterface


class PressureSensor():
    """An interface for initializing and getting calibrated data from a
    SPL06-007 pressure sensor.  The data sheet for the sensor can be
    found at
    https://datasheet.lcsc.com/szlcsc/1912111437_Goertek-SPL06-007_C233787.pdf
    """

    def __init__(self, dump_communication=False):
        self._communicator = Communicator(
            dump_communication=dump_communication)
        self._sampling_set = False
        self._first_measurement_has_happened = False

    def __enter__(self):
        return self._communicator.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._communicator.__exit__(exc_type, exc_val, exc_tb)

    def close(self):
        """Deinitializes and unlocks the I2C bus."""
        self._communicator.close()

    def is_present(self):
        return self._communicator.is_present()

    def set_sampling(self,
                     pressure_oversample=16,
                     pressure_sampling_rate=1,
                     temperature_oversample=1,
                     temperature_sampling_rate=1):
        """Set the amount of oversampling and the sampling rate

        Parameters
        ----------
        pressure_oversample=16 : {1, 2, 4, 8, 16, 32, 64, 128}
            The SPL06-007 reads the sensor multiple times and combines
            them into one result to achieve a higher precision. This
            increases the current consumption and the measurement time,
            which again reduces the maximum measurement rate.
            The measurement times and precision for each oversample are
            these values.
            | Oversampling | Measurement time [ms] | Precision [PaRMS] |
            |--------------|-----------------------|-------------------|
            |            1 |                   3.6 |                 5 |
            |            2 |                   5.2 |                   |
            |            4 |                   8.4 |               2.5 |
            |            8 |                  14.8 |                   |
            |           16 |                  27.6 |               1.2 |
            |           32 |                  53.2 |               0.9 |
            |           64 |                 104.4 |               0.5 |
            |          128 |                 206.8 |                   |
        pressure_sampling_rate=1 : {1, 2, 4, 8, 16, 32, 64, 128}
            The sampling rate of for pressure in hertz.  The sampling
            rate is only relevant in Background Mode.
        temperature_oversample=1 : {1, 2, 4, 8, 16, 32, 64, 128}
            The SPL06-007 reads the sensor multiple times and combines
            them into one result to achieve a higher precision. This
            increases the current consumption and the measurement time,
            which again reduces the maximum measurement rate.
            Setting the oversample for temperature is optional and may
            not be relevant.
            The measurement time for oversample=1 is 3.6 ms.
        temperature_sampling_rate=1 : {1, 2, 4, 8, 16, 32, 64, 128}
            The sampling rate for temperature in hertz.  The sampling
            rate is only relevant in Background Mode.
        """
        self._communicator.set_pressure_sampling(
            oversample=pressure_oversample,
            rate=pressure_sampling_rate
        )
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
        """Sets the mode in which the sensor samples data

        Parameters
        ----------
        op_mode: {self.OpMode.standby,
                  self.OpMode.background,
                  self.OpMode.command}
            self.OpMode.standby is the default mode after power on or
            reset.  No measurements are performed.  All registers and
            compensation coefficients are accessible.
            In self.OpMode.background, pressure and/or temperature
            measurements are performed continuously according to the
            selected measurement precision and rate. The temperature
            measurement is performed immediately after the pressure
            measurement.  The FIFO can be used to store 32 measurement
            results and minimize the number of times the sensor must be
            accessed to read out the results.
            In self.OpMode.command, one temperature or pressure
            measurement is performed according to the selected
            precision.  The sensor will return to Standby Mode when the
            measurement is finished, and the measurement result will be
            available in the data registers.
        """
        return self._communicator.set_op_mode(op_mode)

    def pressure(self):
        """Returns the currect pressure in Pa.  If set_sampling() has
        not been called, then it will return NaN.
        """
        if self._sampling_set:
            self._first_measurement_delay()
            return self._calibrator.pressure(
                self._communicator.raw_pressure(),
                self._communicator.raw_temperature()
            )
        else:
            return float("nan")

    def temperature(self):
        """Returns the currect temperature in degC.  If set_sampling()
        has not been called, then it will return NaN.
        """
        if self._sampling_set:
            self._first_measurement_delay()
            return self._calibrator.temperature(
                self._communicator.raw_temperature()
            )
        else:
            return float("nan")

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
    """Takes raw data from a SPL06-007 pressure sensor and converts it
    to pressure data in Pa and temperature data in degC.
    """

    def __init__(self,
                 calibration_coefficients,
                 pressure_scaling_factor,
                 temperature_scaling_factor):
        """Initializes self.

        Parameters
        ----------
        calibration_coefficients : iterable
            An iterable with the coefficients
            (c0, c1, c00, c10, c01, c11, c20, c21, c30) as defined in the
            data sheet.
        pressure_scaling_factor : int
            A scaling factor corresponding with the selected pressure
            oversampling.
        temperature_scaling_factor : int
            A scaling factor corresponding with the selected temperature
            oversampling
        """
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
        """Pressure in Pa.

        Parameters
        ----------
        raw_pressure : int
            Raw pressure from the sensor.
        raw_temperature : int
            Raw temperature from the sensor.
        """
        scaled_pressure = raw_pressure / self._pressure_scaling_factor
        scaled_temperature = (raw_temperature
                              / self._temperature_scaling_factor)

        compensated_pressure = (
            self._c00
            + scaled_pressure*(self._c10
                               + scaled_pressure*(self._c20
                                                  + scaled_pressure*self._c30)
                               )
            + scaled_temperature*self._c01
            + scaled_temperature*scaled_pressure*(self._c11
                                                  + scaled_pressure*self._c21)
        )
        return compensated_pressure

    def temperature(self, raw_temperature):
        """Temperature in degC

        Parameters
        ----------
        raw_temperature : int
            Raw temperature from the sensor.
        """
        scaled_temperature = (raw_temperature
                              / self._temperature_scaling_factor)
        compensated_temperature = (
            self._c0 * 0.5 + self._c1 * scaled_temperature
        )
        return compensated_temperature


class Communicator():
    """Performs I2C communication between a Raspberry Pi and a
    SPL06-007 pressure sensor.

    Parameters
    ----------
    SDO_high=True: bool
        Set to false if the SDO pin on the SPL06-007 is pulled to ground
    dump_communication=False: bool
        For every read or write to the I2C device, the transmitted and
        recieved communication will be printed alongside the time in
        millis since epoch.  A write will look like this,
            1594169517918.1819 TX -> 0x0C09
        and a read will look like this.
            1594169517938.8496 TX -> 0x08
            1594169517939.2563 RX <- 0x40
    """

    _READY_WAIT_TIME = 0.0036

    def __init__(self, SDO_high=True, dump_communication=False):
        """The sensor takes(107 + /- 8) ms to initialize."""
        if SDO_high:
            self._i2c_address = SensorConstants.DEVICE_ADDRESS_SDO_HIGH
        else:
            self._i2c_address = SensorConstants.DEVICE_ADDRESS_SDO_LOW
        self._i2c = I2CInterface(self._i2c_address,
                                 dump_communication=dump_communication)
        self._i2c.find_device()
        self._reset_sensor()
        self.set_op_mode(PressureSensor.OpMode.standby)
        self._calculate_calibration_coefficients()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Deinitializes and unlocks the I2C bus."""
        self._i2c.close()

    def is_present(self):
        if self._i2c_address in self._i2c.scan():
            return True
        else:
            return False

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
            self._i2c.write_register(
                SensorConstants.SENSOR_OP_MODE,
                SensorConstants.BACKGROUND_PRESSURE_TEMPERATURE
            )
            self._op_mode = PressureSensor.OpMode.background
            return PressureSensor.OpMode.background

        else:
            if mode != PressureSensor.OpMode.standby:
                warnings.warn("Undefined mode.  Defaulting to"
                              "Standby Mode",
                              RuntimeWarning)
            set_standby = True
        if set_standby:
            self._i2c.write_register(
                SensorConstants.SENSOR_OP_MODE, SensorConstants.STANDBY)
            self._op_mode = PressureSensor.OpMode.standby
            return PressureSensor.OpMode.standby

    @property
    def calibration_coefficients(self):
        """The calibration coefficients
        (c0, c1, c00, c10, c01, c11, c20, c21, c30)
        """
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
            rate_mode = SensorConstants.PRESSURE_RATE_OPTIONS[rate]
        except KeyError:
            raise ValueError("Pressure sampling rate can only be "
                             "1, 2, 4, 8, 16, 32, 64, or 128 Hz")
        try:
            oversample_mode = (
                SensorConstants.PRESSURE_OVERSAMPLE_OPTIONS[oversample]
            )
            self._pressure_scale_factor = (
                SensorConstants.COMPENSATION_SCALE_FACTORS[oversample]
            )
        except KeyError:
            raise ValueError("Pressure oversampling can only be "
                             "1, 2, 4, 8, 16, 32, 64, or 128X")
        self._i2c.write_register(SensorConstants.PRESSURE_CONFIGURATION,
                                 rate_mode | oversample_mode)
        if oversample > 8:
            self._i2c.write_register(
                SensorConstants.INTERRUPT_AND_FIFO_CONFIGURATION,
                SensorConstants.PRESSURE_RESULT_BIT_SHIFT
            )
        else:
            new_interrupt_and_fifo_config_state = (
                self._i2c.read_register(
                    SensorConstants.INTERRUPT_AND_FIFO_CONFIGURATION
                ) & (0xff - SensorConstants.PRESSURE_RESULT_BIT_SHIFT))
            self._i2c.write_register(
                SensorConstants.INTERRUPT_AND_FIFO_CONFIGURATION,
                new_interrupt_and_fifo_config_state
            )

    def raw_pressure(self):
        """The raw pressuring reading from the sensor.  This needs to
        be scaled and compensated per the data sheet to be useful.
        """
        if self._op_mode == PressureSensor.OpMode.command:
            self._i2c.write_register(
                SensorConstants.SENSOR_OP_MODE,
                SensorConstants.COMMAND_PRESSURE
            )

        def pressure_ready():
            return (self._i2c.read_register(SensorConstants.SENSOR_OP_MODE)
                    & SensorConstants.PRS_RDY != 0)
        self._wait_for_condition_else_timeout(pressure_ready, 4)

        pressure_msb = self._i2c.read_register(
            SensorConstants.PRESSURE_MSB)
        pressure_lsb = self._i2c.read_register(
            SensorConstants.PRESSURE_LSB)
        pressure_xlsb = self._i2c.read_register(
            SensorConstants.PRESSURE_XLSB)

        pressure = self._twos_complement(((pressure_msb << 16)
                                          + (pressure_lsb << 8)
                                          + pressure_xlsb),
                                         24)
        return pressure

    @property
    def pressure_scale_factor(self):
        """A constant used for calibrating the sensor."""
        return self._pressure_scale_factor

    def set_temperature_sampling(self, oversample=1, rate=1):
        """Set the amount of oversampling and the sampling rate.

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
            rate_mode = SensorConstants.TEMPERATURE_RATE_OPTIONS[rate]
        except KeyError:
            raise ValueError("Temperature sampling rate can only be "
                             "1, 2, 4, 8, 16, 32, 64, or 128 Hz")
        try:
            oversample_mode = (
                SensorConstants.TEMPERATURE_OVERSAMPLE_OPTIONS[oversample]
            )
            self._temperature_scale_factor = \
                SensorConstants.COMPENSATION_SCALE_FACTORS[oversample]
        except KeyError:
            raise ValueError("Temperature oversampling can only be "
                             "1, 2, 4, 8, 16, 32, 64, or 128X")
        self._i2c.write_register(SensorConstants.TEMPERATURE_CONFIGURATION,
                                 rate_mode | oversample_mode)
        if oversample > 8:
            self._i2c.write_register(
                SensorConstants.INTERRUPT_AND_FIFO_CONFIGURATION,
                SensorConstants.TEMPERATURE_RESULT_BIT_SHIFT
            )
        else:
            new_interrupt_and_fifo_config_state = (
                self._i2c.read_register(
                    SensorConstants.INTERRUPT_AND_FIFO_CONFIGURATION)
            ) & (0xff - SensorConstants.TEMPERATURE_RESULT_BIT_SHIFT)
            self._i2c.write_register(
                SensorConstants.INTERRUPT_AND_FIFO_CONFIGURATION,
                new_interrupt_and_fifo_config_state
            )

    def raw_temperature(self):
        """The raw temperature reading from the sensor.  This need to
        be scaled and compensated per the data sheet to be useful.
        """
        if self._op_mode == PressureSensor.OpMode.command:
            self._i2c.write_register(SensorConstants.SENSOR_OP_MODE,
                                     SensorConstants.COMMAND_TEMPERATURE)

        def temperature_ready():
            return (self._i2c.read_register(SensorConstants.SENSOR_OP_MODE)
                    & SensorConstants.TMP_RDY != 0)
        self._wait_for_condition_else_timeout(temperature_ready, 4)

        temperature_msb = self._i2c.read_register(
            SensorConstants.TEMPERATURE_MSB)
        temperature_lsb = self._i2c.read_register(
            SensorConstants.TEMPERATURE_LSB)
        temperature_xlsb = self._i2c.read_register(
            SensorConstants.TEMPERATURE_XLSB)
        temperature = self._twos_complement(((temperature_msb << 16)
                                             + (temperature_lsb << 8)
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
        def coefficients_ready():
            return (self._i2c.read_register(SensorConstants.SENSOR_OP_MODE)
                    & SensorConstants.COEF_RDY != 0)
        self._wait_for_condition_else_timeout(coefficients_ready, 4)

        _c0_11_4 = self._i2c.read_register(SensorConstants.C0_11_4)
        _c0_3_0_c1_11_8 = (
            self._i2c.read_register(SensorConstants.C0_3_0_C1_11_8))
        _c1_7_0 = self._i2c.read_register(SensorConstants.C1_7_0)
        _c00_19_12 = self._i2c.read_register(SensorConstants.C00_19_12)
        _c00_11_4 = self._i2c.read_register(SensorConstants.C00_11_4)
        _c00_3_0_c10_19_16 = (
            self._i2c.read_register(SensorConstants.C00_3_0_C10_19_16))
        _c10_15_8 = self._i2c.read_register(SensorConstants.C10_15_8)
        _c10_7_0 = self._i2c.read_register(SensorConstants.C10_7_0)
        _c01_15_8 = self._i2c.read_register(SensorConstants.C01_15_8)
        _c01_7_0 = self._i2c.read_register(SensorConstants.C01_7_0)
        _c11_15_8 = self._i2c.read_register(SensorConstants.C11_15_8)
        _c11_7_0 = self._i2c.read_register(SensorConstants.C11_7_0)
        _c20_15_8 = self._i2c.read_register(SensorConstants.C20_15_8)
        _c20_7_0 = self._i2c.read_register(SensorConstants.C20_7_0)
        _c21_15_8 = self._i2c.read_register(SensorConstants.C21_15_8)
        _c21_7_0 = self._i2c.read_register(SensorConstants.C21_7_0)
        _c30_15_8 = self._i2c.read_register(SensorConstants.C30_15_8)
        _c30_7_0 = self._i2c.read_register(SensorConstants.C30_7_0)

        def most_significant_nibble(byte): return (byte & 0xf0) >> 4

        def least_significant_nibble(byte): return byte & 0x0f

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

    def _reset_sensor(self):
        reset_time = 0.02
        self._i2c.write_register(SensorConstants.RESET_AND_FLUSH,
                                 SensorConstants.SOFT_RESET)
        time.sleep(reset_time)

        def sensor_ready(): return (
            self._i2c.read_register(SensorConstants.SENSOR_OP_MODE)
            & SensorConstants.SENSOR_RDY != 0)
        self._wait_for_condition_else_timeout(sensor_ready, 4)

    def _wait_for_condition_else_timeout(self, conditionFunction, timeout):

        start_time = time.time()
        while not conditionFunction():
            if time.time() - start_time > timeout:
                return False
            time.sleep(self._READY_WAIT_TIME)
        return True

    def _twos_complement(self, value, bits):

        if (value & (1 << (bits - 1))) != 0:
            complement = (value & (2**bits - 1)) - (1 << bits)
        else:
            complement = value & (2**bits - 1)
        return complement


class SensorConstants():
    """The names and addresses of every register on the chip and codes
    to write to them
    """
    DEVICE_ADDRESS_SDO_HIGH = 0x77
    DEVICE_ADDRESS_SDO_LOW = 0x76

    # Register addresses
    PRESSURE_MSB = 0x00
    PRESSURE_LSB = 0x01
    PRESSURE_XLSB = 0x02
    TEMPERATURE_MSB = 0x03
    TEMPERATURE_LSB = 0x04
    TEMPERATURE_XLSB = 0x05
    PRESSURE_CONFIGURATION = 0x06
    TEMPERATURE_CONFIGURATION = 0x07
    SENSOR_OP_MODE = 0x08
    INTERRUPT_AND_FIFO_CONFIGURATION = 0x09
    INTERRUPT_STATUS = 0x0A
    FIFO_STATUS = 0x0B
    RESET_AND_FLUSH = 0x0C
    PRODUCT_AND_REVISION_ID = 0x0D
    # Calibration Coefficient register addresses
    C0_11_4 = 0x10
    C0_3_0_C1_11_8 = 0x11
    C1_7_0 = 0x12
    C00_19_12 = 0x13
    C00_11_4 = 0x14
    C00_3_0_C10_19_16 = 0x15
    C10_15_8 = 0x16
    C10_7_0 = 0x17
    C01_15_8 = 0x18
    C01_7_0 = 0x19
    C11_15_8 = 0x1A
    C11_7_0 = 0x1B
    C20_15_8 = 0x1C
    C20_7_0 = 0x1D
    C21_15_8 = 0x1E
    C21_7_0 = 0x1F
    C30_15_8 = 0x20
    C30_7_0 = 0x21

    # Bitmasks to read from registers
    #   Read these from self._SENSOR_OP_MODE
    COEF_RDY = 0b10000000
    SENSOR_RDY = 0b01000000
    TMP_RDY = 0b00100000
    PRS_RDY = 0b00010000
    #   Read these from self._INTERRUPT_STATUS
    INT_FIFO_FULL = 0b00000100
    INT_TMP = 0b00000010
    INT_PRS = 0b00000001
    #   Read these from self._FIFO_STATUS
    FIFO_FULL = 0b00000010
    FIFO_EMPTY = 0b00000001
    #   Read these from self._PRODUCT_AND_REVISION_ID
    PROD_ID = 0b11110000
    REV_ID = 0b00001111

    # Codes to write to registers
    #   Write these to self._PRESSURE_CONFIGURATION
    #   The rate and oversample can bitwise-or'ed together
    PRESSURE_RATE_1HZ = 0b00000000
    PRESSURE_RATE_2HZ = 0b00010000
    PRESSURE_RATE_4HZ = 0b00100000
    PRESSURE_RATE_8HZ = 0b00110000
    PRESSURE_RATE_16HZ = 0b01000000
    PRESSURE_RATE_32HZ = 0b01010000
    PRESSURE_RATE_64HZ = 0b01100000
    PRESSURE_RATE_128HZ = 0b01110000
    PRESSURE_OVERSAMPLE_1X = 0b00000000
    PRESSURE_OVERSAMPLE_2X = 0b00000001
    PRESSURE_OVERSAMPLE_4X = 0b00000010
    PRESSURE_OVERSAMPLE_8X = 0b00000011
    PRESSURE_OVERSAMPLE_16X = 0b00000100
    PRESSURE_OVERSAMPLE_32X = 0b00000101
    PRESSURE_OVERSAMPLE_64X = 0b00000110
    PRESSURE_OVERSAMPLE_128X = 0b00000111
    #   Write these to self._TEMPERATURE_CONFIGURATION
    #   The sensor, rate, and can be bitwise-or'ed together
    TEMPERATURE_SENSOR_INTERNAL = 0b10000000
    TEMPERATURE_SENSOR_EXTERNAL = 0b00000000
    TEMPERATURE_RATE_1HZ = 0b00000000
    TEMPERATURE_RATE_2HZ = 0b00010000
    TEMPERATURE_RATE_4HZ = 0b00100000
    TEMPERATURE_RATE_8HZ = 0b00110000
    TEMPERATURE_RATE_16HZ = 0b01000000
    TEMPERATURE_RATE_32HZ = 0b01010000
    TEMPERATURE_RATE_64HZ = 0b01100000
    TEMPERATURE_RATE_128HZ = 0b01110000
    TEMPERATURE_OVERSAMPLE_1X = 0b00000000
    TEMPERATURE_OVERSAMPLE_2X = 0b00000001
    TEMPERATURE_OVERSAMPLE_4X = 0b00000010
    TEMPERATURE_OVERSAMPLE_8X = 0b00000011
    TEMPERATURE_OVERSAMPLE_16X = 0b00000100
    TEMPERATURE_OVERSAMPLE_32X = 0b00000101
    TEMPERATURE_OVERSAMPLE_64X = 0b00000110
    TEMPERATURE_OVERSAMPLE_128X = 0b00000111
    #   Write these to self._SENSOR_OP_MODE
    STANDBY = 0b00000000
    COMMAND_PRESSURE = 0b00000001
    COMMAND_TEMPERATURE = 0b00000010
    BACKGROUND_PRESSURE = 0b00000101
    BACKGROUND_TEMPERATURE = 0b00000110
    BACKGROUND_PRESSURE_TEMPERATURE = 0b00000111
    #  Read or write these to self._INTERRUPT_AND_FIFO_CONFIGURATION
    #  Note: temperature or pressure bit shift must be set when
    #  their respective oversample rates are set to > 8
    SET_INTERRUPT_ACTIVE_LEVEL = 0b10000000
    GENERATE_INTERRUPT_WHEN_FIFO_IS_FULL = 0b01000000
    GENERATE_INTERRUPT_WHEN_PRESSURE_IS_READY = 0b00100000
    GENERATE_INTERRUPT_WHEN_TEMPERATURE_IS_READY = 0b00010000
    TEMPERATURE_RESULT_BIT_SHIFT = 0b00001000
    PRESSURE_RESULT_BIT_SHIFT = 0b00000100
    ENABLE_FIFO = 0b00000010
    SET_4_WIRE_SPI = 0b00000000
    SET_3_WIRE_SPI = 0b00000001
    #   Write these to self._RESET_AND_FLUSH
    #   They can be bitwise-or'ed together
    FLUSH_FIFO = 0b10000000
    SOFT_RESET = 0b00001001

    # For use in calibrating the sensor, taken from Table 4 of
    # the data sheet
    COMPENSATION_SCALE_FACTORS = {1: 524288,
                                  2: 1572864,
                                  4: 3670016,
                                  8: 7864320,
                                  16: 253952,
                                  32: 516096,
                                  64: 1040384,
                                  128: 2088960}

    # Some helper constants
    PRESSURE_RATE_OPTIONS = {1: PRESSURE_RATE_1HZ,
                             2: PRESSURE_RATE_2HZ,
                             4: PRESSURE_RATE_4HZ,
                             8: PRESSURE_RATE_8HZ,
                             16: PRESSURE_RATE_16HZ,
                             32: PRESSURE_RATE_32HZ,
                             64: PRESSURE_RATE_64HZ,
                             128: PRESSURE_RATE_128HZ}
    PRESSURE_OVERSAMPLE_OPTIONS = {1: PRESSURE_OVERSAMPLE_1X,
                                   2: PRESSURE_OVERSAMPLE_2X,
                                   4: PRESSURE_OVERSAMPLE_4X,
                                   8: PRESSURE_OVERSAMPLE_8X,
                                   16: PRESSURE_OVERSAMPLE_16X,
                                   32: PRESSURE_OVERSAMPLE_32X,
                                   64: PRESSURE_OVERSAMPLE_64X,
                                   128: PRESSURE_OVERSAMPLE_128X}
    TEMPERATURE_RATE_OPTIONS = {1: TEMPERATURE_RATE_1HZ,
                                2: TEMPERATURE_RATE_2HZ,
                                4: TEMPERATURE_RATE_4HZ,
                                8: TEMPERATURE_RATE_8HZ,
                                16: TEMPERATURE_RATE_16HZ,
                                32: TEMPERATURE_RATE_32HZ,
                                64: TEMPERATURE_RATE_64HZ,
                                128: TEMPERATURE_RATE_128HZ}
    TEMPERATURE_OVERSAMPLE_OPTIONS = {1: TEMPERATURE_OVERSAMPLE_1X,
                                      2: TEMPERATURE_OVERSAMPLE_2X,
                                      4: TEMPERATURE_OVERSAMPLE_4X,
                                      8: TEMPERATURE_OVERSAMPLE_8X,
                                      16: TEMPERATURE_OVERSAMPLE_16X,
                                      32: TEMPERATURE_OVERSAMPLE_32X,
                                      64: TEMPERATURE_OVERSAMPLE_64X,
                                      128: TEMPERATURE_OVERSAMPLE_128X}
