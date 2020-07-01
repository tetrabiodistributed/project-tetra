import constants
from tca9548a import I2CMux
import board
import busio
import sys
from pathlib import Path
sys.path.append(str(Path(".").absolute().parent))


pressure_sensor_mux = I2CMux(constants.PRESSURE_SENSOR_MUX_ADDRESS)

print(f"Initial scan:\t\t{pressure_sensor_mux.scan()}")

for i in range(8):
    pressure_sensor_mux.select_channel(i)
    print(f"{constants.PRESSURE_SENSOR_MUX_ADDRESS:#x} Mux Port {i}:"
          f"\t{pressure_sensor_mux.scan()}")
pressure_sensor_mux.close()

flow_sensor_mux = I2CMux(constants.FLOW_SENSOR_MUX_ADDRESS)

for i in range(8):
    flow_sensor_mux.select_channel(i)
    print(f"{constants.FLOW_SENSOR_MUX_ADDRESS:#x} Mux Port {i}:"
          f"\t{flow_sensor_mux.scan()}")
flow_sensor_mux.close()
