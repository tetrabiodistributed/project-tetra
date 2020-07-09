How to Use the SPL06-007 Pressure Sensor
========================================

The SPL06-007 is a calibrated pressure sensor often used for drone applications.  This describes how to use the sensor via it's I2C interface, though it'd only really be a change in the first step to use a 3- or 4-wire SPI interface (and in hardware of course).  Note that I connected the sensor to a Raspberry Pi via an I2C multiplexor (mux), so the second step isn't necessary if you don't have that.

- To initialize I2C, I use Adafruit's busio.I2C(board.SCL, board.SDA)
- For the mux select, I write a [0-4] integer to 0x70 (there's also a mux on 0x74, but I don't have anything connected to it right now, so it doesn't do anything.
- I then reset the sensor to clear any previous state by writing 0b1001 to 0x0C
- After that, I set the sensor into standby mode by writing 0 to 0x08
- Then in the case of the tests I'm having issues with, I set the sensor to measure pressure at 1Hz with 16 measurements per sample by writing 0 | 0b0100 to 0x06.  Because there are more than 8 measurements per sample, I also set the sensor to bit shift the pressure by writing 0b0100 to 0x09.
- I do the same to get the temperature, but now it's 1Hz 1 sample, so 0 | 0 gets written to 0x07.
- Then I set the op mode to "command-pressure" by writing 0b0001 to 0x08 so I can read out what the current pressure is.
- After waiting a few milliseconds for the measurement to be ready, I read addresses 0x00, 0x01, and 0x02 to get the pressure measurement.
- Then the op mode is changed to "command-temperature" by writing 0b0010 to 0x08.
- Finally, I read the temperature measurement from 0x03, 0x04, and 0x05

