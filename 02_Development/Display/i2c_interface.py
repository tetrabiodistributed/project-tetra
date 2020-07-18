from abc import ABC, abstractmethod
import random
import warnings
import time
import math


class I2CInterfaceBase(ABC):
    """Implements an I2C interface using adafruit_blinka.

    Parameters
    ----------
    address: int
        The address of the I2C device you want to communicate with.
    dump_communication=False: bool
        For every read or write to the I2C device, the transmitted and
        recieved communication will be printed alongside the time in
        millis since epoch.  A write will look like this,
            1594169517918.1819 TX -> 0x0c09
        and a read will look like this.
            1594169517938.8496 TX -> 0x08
            1594169517939.2563 RX <- 0x40
    """
    @abstractmethod
    def __init__(self, address, dump_communication=False):
        super().__init__()

    @abstractmethod
    def close(self):
        """Deinitializes and unlocks the I2C bus."""
        pass

    @abstractmethod
    def scan(self):
        """Returns a list of all visible I2C addresses."""
        pass

    @abstractmethod
    def find_device(self, timeout=5):
        """Delays until the device is visible on the I2C bus.

        Parameters
        ----------
        timeout=5: float
            The amount of time in seconds this method will search for
            the device before raising a DeviceNotFoundError.
        """
        pass

    @abstractmethod
    def read_register(self, register, number_of_bytes=1):
        """Returns the contents of the bytes located at address address
        on the device.

        Parameters
        ----------
        register: int
            The device register you're interested in.
        number_of_bytes=1: int > 0
            The number of bytes you'd like to read from that register.
        """
        pass

    @abstractmethod
    def read_data(self, number_of_bytes=1):
        """Returns the contents of whats on the I2C bus.

        Parameters
        ----------
        number_of_bytes=1: int > 0
            The number of bytes you'd like to read from the bus.
        """

    @abstractmethod
    def write_register(self, register, to_write):
        """Writes to_write to register

        Parameters
        ----------
        register: int
            The device register you're interested in.
        to_write: int
            The data you'd like to write to that register.
        """
        pass

    @abstractmethod
    def write_data(self, byte):
        """Writes a single byte to the the device address.

        Parameters
        ----------
        byte: int
            The byte you'd like to write to the device address.
        """


try:

    import board
    import busio

    class I2CInterface(I2CInterfaceBase):

        def __init__(self, address, dump_communication=False):
            self._i2c_address = address
            self._dump_communication = dump_communication
            self._i2c = busio.I2C(board.SCL, board.SDA)
            while not self._i2c.try_lock():
                pass

        def close(self):
            self._i2c.unlock()
        
        def scan(self):
            return self._i2c.scan()

        def find_device(self, timeout=5):
            start_time = time.time()
            while not self._i2c_address in self.scan():
                if time.time() - start_time > timeout:
                    raise DeviceNotFoundError("Could not find I2C "
                                              "device at address "
                                              f"{self._i2c_address}")

        def read_register(self, register, number_of_bytes=1):
            return self._read(register=register,
                              number_of_bytes=number_of_bytes)

        def read_data(self, number_of_bytes=1):
            return self._read(number_of_bytes=number_of_bytes)

        def write_register(self, register, to_write):
            self._i2c.writeto(self._i2c_address, bytes([register, to_write]))

            if self._dump_communication:
                print(f"{1000*time.time():.4f} "
                      "TX -> 0x" + bytes([register, to_write]).hex())

        def write_data(self, data):
            byte_data = self._int_to_bytearray(data)
            self._i2c.writeto(self._i2c_address, byte_data)

            if self._dump_communication:
                print(f"{1000*time.time():.4f} TX -> 0x" + byte_data.hex())

        def _read(self, register=None, number_of_bytes=1):
            if number_of_bytes < 1:
                raise ValueError("Cannot read fewer than 1 byte.")

            data = bytearray(number_of_bytes)
            byte_register = bytearray()
            if register is not None:
                byte_register = self._int_to_bytearray(register)
                self._i2c.writeto(self._i2c_address, byte_register)
            self._i2c.readfrom_into(self._i2c_address,
                                    data,
                                    end=number_of_bytes)

            if self._dump_communication:
                if register is not None:
                    print(f"{1000*time.time():.4f} TX -> 0x"
                          + byte_register.hex())
                print(f"{1000*time.time():.4f} RX <- 0x{data.hex()}")

            if number_of_bytes == 1:
                return int(data.hex(), 16)
            else:
                return tuple(byte for byte in data)

        def _int_to_bytearray(self, integer):
            if integer != 0:
                return (
                    bytearray(
                        reversed([(integer >> 8*i) & 0xff
                                  for i in range(math.ceil((math.log2(integer)
                                                              +1)/8))])))
            else:
                return bytearray([0])


except ModuleNotFoundError:

    class I2CInterface(I2CInterfaceBase):
        def __init__(self, address, dump_communication=False):
            self._dump_communication = dump_communication
            warnings.warn("I2C communication is not available on this "
                          "hardware.  All data over I2C will be random "
                          "numbers.",
                          UserWarning)

        def close(self):
            pass

        def scan(self):
            return [random.randrange(0, 0x80)
                    for _ in range(random.randrange(0, 10))]

        def find_device(self, timeout=5):
            pass

        def read_register(self, register, number_of_bytes=1):
            return self._read(register=register,
                              number_of_bytes=number_of_bytes)

        def read_data(self, number_of_bytes=1):
            return self._read(number_of_bytes=number_of_bytes)

        def write_register(self, register, to_write):
            time.sleep(0.0003)
            if self._dump_communication:
                print(f"{1000*time.time():.4f} "
                      f"TX -> 0x" + bytes([register, to_write]).hex())

        def write_data(self, byte):
            if self._dump_communication:
                print(f"{1000*time.time():.4f} TX -> 0x"
                      + bytes([byte]).hex())

        def _read(self, register=None, number_of_bytes=1):
            if number_of_bytes < 1:
                raise ValueError("Cannot read fewer than 1 byte.")

            time.sleep(0.0002)
            if number_of_bytes == 1:
                data = random.randrange(0, 255)
            else:
                data = tuple(random.randrange(0, 255)
                             for _ in range(number_of_bytes))

            if self._dump_communication:
                if register is not None:
                    print(f"{1000*time.time():.4f} TX -> 0x"
                          + bytes([register]).hex())
                rx_string = [f"{1000*time.time():.4f} RX <- 0x"]
                if number_of_bytes > 1:
                    rx_string.extend([f"{data[i]:02X}"
                                      for i in range(number_of_bytes)])
                else:
                    rx_string.append(f"{data:02X}")
                print("".join(rx_string))

            return data


class DeviceNotFoundError(Exception):
    pass
