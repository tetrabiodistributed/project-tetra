import unittest
import math

from sfm3300d import FlowSensor, Calibrator, Communicator, CRCError
from tca9548a import I2CMux
from rpi_check import is_on_raspberry_pi
import constants
from i2c_interface import I2CInterface


class TestFlowSensor(unittest.TestCase):

    def setUp(self):
        self._mux = I2CMux(constants.FLOW_SENSOR_MUX_ADDRESS)
        self._mux.select_channel(2)
        self._sensor = FlowSensor()

    def tearDown(self):
        self._sensor.close()
        self._mux.close()

    def test_serial_number(self):
        serial_number = self._sensor.serial_number()
        self.assertTrue(0 <= serial_number < 2**32,
                        f"{serial_number} is not an unsigned 32-bit "
                        "serial number")

    @unittest.skipIf(not is_on_raspberry_pi(),
                     "Cannot determine ambient flow unless connected "
                     "to hardware.")
    def test_ambient_flow(self):
        measured_flow = self._sensor.flow()
        self.assertTrue(math.isclose(measured_flow, 0,
                                     abs_tol=1),
                        f"{measured_flow} != 0 +/- 0.1 slm : "
                        "Fails to say that there is no flow in still "
                        "air.\n"
                        "Note that if this test is performed in a "
                        "breezy environment, then the ambient flow may "
                        "fall ouside the range of this test.")


class TestCalibrator(unittest.TestCase):

    def test_zero_one_parameters_and_zero_data(self):
        calibrator = Calibrator(0, 1)
        self.assertAlmostEqual(calibrator.flow(0), 0.0,
                               msg="Fails to return 0.0 when measured "
                               "value and offset flow are zero and "
                               "scale factor flow is non-zero.")

    def test_zero_scale_factor_flow(self):
        with self.assertRaises(ZeroDivisionError,
                               msg="Fails to raise a ZeroDivisionError "
                               "when initialized with a scale factor "
                               "flow equal to 0."):
            Calibrator(0, 0)

    def test_one_parameters_and_data(self):
        calibrator = Calibrator(1, 1)
        self.assertAlmostEqual(calibrator.flow(1), 0.0,
                               msg="Fails to return 0.0 when measured "
                               "value, offset flow, and scale factor "
                               "flow are one.")

    def test_one_parameters_and_large_data(self):
        calibrator = Calibrator(1, 1)
        self.assertAlmostEqual(calibrator.flow(10), 9.0,
                               msg="Fails to return the correct value "
                               "when the result is non-zero.")

    def test_actual_data(self):
        calibrator = Calibrator(32768, 120)
        self.assertAlmostEqual(calibrator.flow(32780), 0.1,
                               msg="Fails to return a reasonable value "
                               "given actual data the sensor could "
                               "return.")


class TestCommunicator(unittest.TestCase):

    def setUp(self):
        self._mux = I2CMux(constants.FLOW_SENSOR_MUX_ADDRESS)
        self._mux.select_channel(2)
        self._communicator = Communicator()

    def tearDown(self):
        self._communicator.close()
        self._mux.close()

    def test_is_present(self):
        self.assertTrue(self._communicator.is_present(),
                        "Sensor is not useable at the moment.")

    def test_serial_number(self):
        serial_number = self._communicator.serial_number()
        self.assertTrue(0 <= serial_number < 2**32,
                        f"{serial_number:#x} is not an unsigned 32-bit "
                        "serial number.")

    @unittest.skipIf(not is_on_raspberry_pi(),
                     "Signal isn't 2 bytes + CRC8 unless connected "
                     "to hardware.")
    def test_raw_flow(self):
        self._communicator.init_flow()
        raw_flow = self._communicator.raw_flow()
        self.assertTrue(0 <= raw_flow < 2**16,
                        f"{raw_flow:#x} is not an unsigned 16-bit flow "
                        "number.")

    # @unittest.skipIf(is_on_raspberry_pi(),
    #                  "The signal cannot be automatically be made to "
    #                  "fail on hardware.")
    # def test_raises_CRCError(self):
    #     """I'm not sure how to make this test fail.  It definitely fails
    #     when not on a Pi, but on the Pi it's at the mercy of whether
    #     there's actually a bad signal.
    #     """
    #     self._communicator.init_flow()
    #     with self.assertRaises(CRCError,
    #                            msg="Fails to raise an error when invalid "
    #                            "data is received."):
    #         self._communicator.raw_flow()
