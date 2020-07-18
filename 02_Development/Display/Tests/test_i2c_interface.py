import unittest
import warnings

from i2c_interface import I2CInterface, DeviceNotFoundError
from rpi_check import is_on_raspberry_pi


class TestI2CInterface(unittest.TestCase):

    def setUp(self):
        warnings.filterwarnings("ignore",
                                message="I2C communication",
                                category=UserWarning)
        self._i2c = I2CInterface(0x70)

    def tearDown(self):
        self._i2c.close()

    def test_warn_when_i2c_isnt_available(self):
        if not is_on_raspberry_pi():
            self._i2c.close()
            with self.assertWarns(UserWarning,
                                  msg="Fails to warn the user when I2C "
                                  "communication isn't available."):
                self._i2c = I2CInterface(0x70)

    def test_read_returns_a_byte(self):
        self.assertTrue(0 <= self._i2c.read_register(0x00) < 256,
                        "Fails to return a byte when a register is "
                        "read")

    def test_read_returns_several_bytes(self):
        self.assertEqual(len(self._i2c.read_register(0x00,
                                                     number_of_bytes=3)),
                         3,
                         "Fails to read several bytes from a single "
                         "read.")

    def test_read_fewer_than_one_byte(self):
        with self.assertRaises(ValueError,
                               msg="Fails to raise a ValueError when "
                               "fewer than 1 byte is requested."):
            self._i2c.read_register(0x00, 0)

    def test_read_from_bus(self):
        self.assertTrue(0 <= self._i2c.read_data() < 256,
                        "Fails to return a byte when the bus is read")
