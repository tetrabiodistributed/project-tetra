from i2c_interface import I2CInterface


class I2CMux():

    def __init__(self, mux_address):
        self._i2c = I2CInterface(mux_address)

    def close(self):
        self._i2c.close()

    def select_channel(self, channel):
        if channel > 7:
            raise ValueError("Multiplexor channel must be an integer 0-7")
        else:
            self._i2c.write_data(1 << channel)

    def scan(self):
        return self._i2c.scan()
