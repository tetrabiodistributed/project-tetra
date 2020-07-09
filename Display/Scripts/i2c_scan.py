import board
import busio

i2c = busio.I2C(board.SCL, board.SDA)

def mux_select(channel, mux_address):
    if channel > 7:
            raise ValueError("Multiplexor channel must be an integer 0-7")
    else:
        busio.I2C(board.SCL, board.SDA).writeto(mux_address,
                                                bytes([1 << channel]))


initial_scan = i2c.scan()
print(f"Initial scan:\t{initial_scan}")
for address in initial_scan:
    for i in range(8):
        mux_select(i, address)
        print(f"{address} Mux Port {i}:\t{i2c.scan()}")
