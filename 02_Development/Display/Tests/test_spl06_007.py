import unittest
import math
import warnings

from spl06_007 import (PressureSensor,
                       Communicator,
                       Calibrator,
                       SensorConstants)
from i2c_interface import I2CInterface
from tca9548a import I2CMux
from rpi_check import is_on_raspberry_pi
import constants


class TestPressureSensor(unittest.TestCase):

    def setUp(self):
        self._mux = I2CMux(constants.PRESSURE_SENSOR_MUX_ADDRESS)
        self._mux.select_channel(0)
        self._sensor = PressureSensor()

    def tearDown(self):
        self._sensor.close()
        self._mux.close()

    @unittest.skipIf(not is_on_raspberry_pi(),
                     "Pressure sensor won't be present unless you're on "
                     "hardware.")
    def test_is_present(self):
        self.assertTrue(self._sensor.is_present(),
                        "Fails to identify that the sensor is present.\n"
                        "Note that if the sensor is not connected, this "
                        "test will fail.")

    @unittest.skipIf(is_on_raspberry_pi(),
                     "This can only be tested non-interactively off of "
                     "hardware.")
    def test_not_is_present(self):
        self.assertTrue(not self._sensor.is_present(),
                        "Fails to correctly identify that a sensor is not "
                        "present.")

    def test_set_op_mode_standby(self):
        self.assertEqual(
            self._sensor.set_op_mode(PressureSensor.OpMode.standby),
            PressureSensor.OpMode.standby,
            "Fails to put the sensor into Standby Mode.")

    def test_set_op_mode_background(self):
        self.assertEqual(
            self._sensor.set_op_mode(PressureSensor.OpMode.background),
            PressureSensor.OpMode.background,
            "Fails to put the sensor into Background Mode")

    def test_set_op_mode_command(self):
        self.assertEqual(
            self._sensor.set_op_mode(PressureSensor.OpMode.command),
            PressureSensor.OpMode.command,
            "Fails to put the sensor into Command Mode.")

    def test_set_sampling_default(self):
        self.assertTrue(self._sensor.set_sampling(),
                        "Fails to successfully set the oversample and "
                        "sampling rate to default values for temerature "
                        "and pressure.")

    def test_set_sampling_valid_values(self):
        self.assertTrue(
            self._sensor.set_sampling(pressure_oversample=1,
                                      pressure_sampling_rate=1,
                                      temperature_oversample=1,
                                      temperature_sampling_rate=1),
            "Fails to set the oversample and sampling rate "
            "to valid custom values for temperature and "
            "pressure")

    def test_set_sampling_invalid_values(self):
        with self.assertRaises(ValueError,
                               msg="Fails to raise a ValueError when "
                               "oversample or temperature values are not "
                               "in the set {1, 2, 4, 8, 16, 32, 64, 128}."):
            self._sensor.set_sampling(pressure_oversample=3,
                                      pressure_sampling_rate=3,
                                      temperature_oversample=3,
                                      temperature_sampling_rate=3)

    def test_pressure_without_sampling_set(self):
        self.assertTrue(math.isnan(self._sensor.pressure()),
                        "Fails to return NaN for pressure when the user "
                        "has not yet set the sampling parameters.")
        self.assertTrue(math.isnan(self._sensor.temperature()),
                        "Fails to return NaN for temperature when the "
                        "user has not yet set the sampling parameters.")

    @unittest.skipIf(not is_on_raspberry_pi(),
                     "Cannot determine ambient temperature unless "
                     "connected to hardware.")
    def test_ambient_temperature(self):
        self._sensor.set_op_mode(PressureSensor.OpMode.command)
        self._sensor.set_sampling(temperature_sampling_rate=8)
        measured_temperature = self._sensor.temperature()
        standard_temperature = 20  # degC
        self.assertTrue(math.isclose(measured_temperature,
                                     standard_temperature,
                                     rel_tol=0.50),
                        f"{measured_temperature} != "
                        "20 +/- 50% degC :\n"
                        "Fails to return ambient temperature in "
                        "degC.\nNote that if this test is "
                        "performed in a very cold or hot "
                        "environment, the\nambient temperature "
                        "may fall outside the range of this test.")

    @unittest.skipIf(not is_on_raspberry_pi(),
                     "Cannot determine ambient pressure unless "
                     "connected to hardware.")
    def test_ambient_pressure(self):
        self._sensor.set_sampling()
        self._sensor.set_op_mode(PressureSensor.OpMode.command)
        measured_pressure = self._sensor.pressure()
        standard_pressure = 101325  # Pa
        self.assertTrue(math.isclose(measured_pressure, standard_pressure,
                                     rel_tol=0.10),
                        f"{measured_pressure} != "
                        "101.25 +/- 10% Pa :\n"
                        "Fails to return ambient pressure in Pa.\n"
                        "Note that if this test is performed in a "
                        "very low pressure environment,\nthe ambient "
                        "pressure may fall outside the range of this "
                        "test.")


class TestCalibrator(unittest.TestCase):

    def setUp(self):
        # an example of calibration coefficients gotten from the hardware
        self._hardware_calibration_coefficients = (
            199, -249,
            12179, 14472, -2172, 1284, -7681, -33, -823)

    def test_zero_coefficients_and_data(self):
        calibrator = Calibrator((0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                                1,
                                1)
        self.assertAlmostEqual(calibrator.pressure(0, 0), 0.0,
                               msg="Fails to return 0 pressure when all "
                               "coefficients and data equal 0.")
        self.assertAlmostEqual(calibrator.temperature(0), 0.0,
                               msg="Fails to return 0 temperature when "
                               "all coefficient and data equal 0.")

    def test_zero_coefficients_and_non_zero_data(self):
        calibrator = Calibrator((0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                                1,
                                1)
        self.assertAlmostEqual(calibrator.pressure(10, 10), 0.0,
                               msg="Fails to return 0 pressure when all "
                               "coefficients equal 0.")
        self.assertAlmostEqual(calibrator.temperature(10), 0.0,
                               msg="Fails to return 0 temperature when "
                               "all coefficient equal 0.")

    def test_one_coefficients_and_data(self):
        calibrator = Calibrator((1, 1, 1, 1, 1, 1, 1, 1, 1),
                                1,
                                1)
        self.assertAlmostEqual(calibrator.pressure(1, 1), 7.0,
                               msg="Fails to return 7.0 pressure when "
                               "all coefficients and data equal 1.0.")
        self.assertAlmostEqual(calibrator.temperature(1), 1.5,
                               msg="Fails to return 1.5 temperature "
                               "when all coefficients and data equal 1.0.")

    def test_one_coefficients_and_zero_data(self):
        calibrator = Calibrator((1, 1, 1, 1, 1, 1, 1, 1, 1),
                                1,
                                1)
        self.assertAlmostEqual(calibrator.pressure(0, 0), 1.0,
                               msg="Fails to return 1.0 pressure when "
                               "all coefficients equal 1.0 and data "
                               "equals 0.")
        self.assertAlmostEqual(calibrator.temperature(0), 0.5,
                               msg="Fails to return 1.5 temperature "
                               "when all coefficients equal 1.0 and "
                               "data equals 0.")

    def test_zero_scaling_factor_raises_exception(self):
        with self.assertRaises(ZeroDivisionError,
                               msg="Fails to raise a ZeroDivisionError "
                               "when initialized with a scaling factor "
                               "equal to 0."):
            calibrator = Calibrator((0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                                    0,
                                    0)

    def test_returns_standard_pressure_given_actual_data(self):
        calibrator = Calibrator(self._hardware_calibration_coefficients,
                                253952,
                                524288)
        # Raw pressure and temperature found by solving the compensating
        # equation for raw pressure and temperature given the hardware
        # calibration coefficients.
        # This is true for this and the following few tests.
        self.assertAlmostEqual(calibrator.pressure(-2968390, 167393), 101000,
                               places=-1,
                               msg="Fails to return sea level pressure given "
                               "data that matches that.")

    def test_returns_1_5_atm_pressure_given_actual_data(self):
        calibrator = Calibrator(self._hardware_calibration_coefficients,
                                253952,
                                524288)
        self.assertAlmostEqual(calibrator.pressure(-3053970, 167393), 151500,
                               places=-1,
                               msg="Fails to return 1.5 atm pressure given "
                               "data that matches that.")

    def test_returns_2_atm_pressure_given_actual_data(self):
        calibrator = Calibrator(self._hardware_calibration_coefficients,
                                253952,
                                524288)
        self.assertAlmostEqual(calibrator.pressure(-3132150, 167393), 202000,
                               places=-1,
                               msg="Fails to return 2 atm pressure given "
                               "data that matches that.")

    def test_returns_3_atm_pressure_given_actual_data(self):
        calibrator = Calibrator(self._hardware_calibration_coefficients,
                                253952,
                                524288)
        self.assertAlmostEqual(calibrator.pressure(-3274260, 209505), 303000,
                               places=-1,
                               msg="Fails to return 3 atm pressure given "
                               "data that matches that.")

    def test_return_standard_temperature_given_actual_data(self):
        calibrator = Calibrator(self._hardware_calibration_coefficients,
                                253952,
                                524288)
        self.assertAlmostEqual(calibrator.temperature(167393), 20,
                               places=-1,
                               msg="Fails to return 20degC given data that "
                               "matches that.")

    def test_return_freezing_given_actual_data(self):
        calibrator = Calibrator(self._hardware_calibration_coefficients,
                                253952,
                                524288)
        self.assertAlmostEqual(calibrator.temperature(209505), 0,
                               places=-1,
                               msg="Fails to return 0degC given data that "
                               "matches that.")


class TestCommunicator(unittest.TestCase):

    def setUp(self):
        # A bug in adafruit_platformdetect causes resource warnings
        # to come up in unittest, so the warnings must be filtered out
        # https://github.com/adafruit/Adafruit_Python_PlatformDetect/issues/89
        warnings.filterwarnings("ignore",
                                message="unclosed file",
                                category=ResourceWarning)
        self._mux = I2CMux(constants.PRESSURE_SENSOR_MUX_ADDRESS)
        self._mux.select_channel(0)
        self._communicator = Communicator()

    def tearDown(self):
        self._communicator.close()
        self._mux.close()

    def test_set_op_mode_standby(self):
        self.assertEqual(
            self._communicator.set_op_mode(PressureSensor.OpMode.standby),
            PressureSensor.OpMode.standby,
            "Fails to successfully set the SPL006-007 into standy mode"
        )

    def test_set_op_mode_background(self):
        self.assertEqual(
            self._communicator.set_op_mode(PressureSensor.OpMode.background),
            PressureSensor.OpMode.background,
            "Fails to successfully set the SPL006-007 into background mode"
        )

    def test_set_op_mode_command(self):
        self.assertEqual(
            self._communicator.set_op_mode(PressureSensor.OpMode.command),
            PressureSensor.OpMode.command,
            "Fails to successfully set the SPL006-007 into command mode.")

    def test_set_op_mode_undefined(self):
        with self.assertWarns(RuntimeWarning,
                              msg="Fails to raise a warning when an "
                              "undefined op mode is set."):
            self._communicator.set_op_mode("Undefined Op Mode")

    def test_calibration_coefficients(self):
        self.assertEqual(len(self._communicator.calibration_coefficients), 9,
                         "Fails to generate a list of 9 coefficients.")
        for coefficient in self._communicator.calibration_coefficients:
            self.assertIsInstance(coefficient, int,
                                  "Fails to generate a list of integer "
                                  "coefficients.")

    def test_set_pressure_sampling_sets_scale_factor(self):
        self._communicator.set_pressure_sampling(oversample=16,
                                                 rate=1)
        self.assertEqual(self._communicator.pressure_scale_factor,
                         SensorConstants.COMPENSATION_SCALE_FACTORS[16],
                         "Fails to get the correct pressure scaling "
                         "factor of 253952 for oversampling=16.")

    def test_set_pressure_sampling_invalid_oversample(self):
        with self.assertRaises(ValueError,
                               msg="Fails to raise a ValueError when "
                               "pressure oversample is not in the set "
                               "{1, 2, 4, 8, 16, 32, 64, 128}."):
            self._communicator.set_pressure_sampling(oversample=3)

    def test_set_pressure_sampling_invalid_rate(self):
        with self.assertRaises(ValueError,
                               msg="Fails to raise a ValueError when "
                               "pressure sampling rate is not in the set "
                               "{1, 2, 4, 8, 16, 32, 64, 128}."):
            self._communicator.set_pressure_sampling(rate=3)

    def test_set_temperature_sampling_sets_scale_factor(self):
        self._communicator.set_temperature_sampling(oversample=1,
                                                    rate=1)
        self.assertEqual(self._communicator.temperature_scale_factor,
                         SensorConstants.COMPENSATION_SCALE_FACTORS[1],
                         "Fails to get the correct temperature scaling "
                         "factor of 524288 for oversampling=16.")

    def test_set_op_mode_undefined(self):
        with self.assertWarns(RuntimeWarning,
                              msg="Fails to raise a warning when an "
                              "undefined op mode is set."):
            self._communicator.set_op_mode("Undefined Op Mode")

    def test_calibration_coefficients(self):
        self.assertEqual(len(self._communicator.calibration_coefficients), 9,
                         "Fails to generate a list of 9 coefficients.")
        for coefficient in self._communicator.calibration_coefficients:
            self.assertIsInstance(coefficient, int,
                                  "Fails to generate a list of integer "
                                  "coefficients.")

    def test_set_pressure_sampling_sets_scale_factor(self):
        self._communicator.set_pressure_sampling()
        self.assertEqual(self._communicator.pressure_scale_factor,
                         253952,
                         "Fails to get the correct pressure scaling "
                         "factor of 253952 for oversampling=16.")

    def test_set_pressure_sampling_invalid_oversample(self):
        with self.assertRaises(ValueError,
                               msg="Fails to raise a ValueError when "
                               "pressure oversample is not in the set "
                               "{1, 2, 4, 8, 16, 32, 64, 128}."):
            self._communicator.set_pressure_sampling(oversample=3)

    def test_set_pressure_sampling_invalid_rate(self):
        with self.assertRaises(ValueError,
                               msg="Fails to raise a ValueError when "
                               "pressure sampling rate is not in the set "
                               "{1, 2, 4, 8, 16, 32, 64, 128}."):
            self._communicator.set_pressure_sampling(rate=3)

    def test_raw_temperature(self):
        self._communicator.set_op_mode(PressureSensor.OpMode.command)
        self._communicator.set_temperature_sampling()
        raw_temperature = self._communicator.raw_temperature()
        self.assertIsInstance(
            raw_temperature,
            int,
            "Fails to return raw temperature as an integer.")
        self.assertTrue(-2**23 <= raw_temperature < 2**23,
                        "Fails to return raw temperature as a 24-bit "
                        "2's complement number.")

    def test_raw_temperature(self):
        self._communicator.set_op_mode(PressureSensor.OpMode.command)
        self._communicator.set_pressure_sampling()
        raw_pressure = self._communicator.raw_pressure()
        self.assertIsInstance(raw_pressure, int,
                              "Fails to return raw temperature as an integer.")
        self.assertTrue(-2**23 <= raw_pressure < 2**23,
                        "Fails to return raw temperature as a 24-bit "
                        "2's complement number.")
