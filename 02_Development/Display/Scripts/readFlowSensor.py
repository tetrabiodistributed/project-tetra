import serial
from datetime import datetime


if __name__ == "__main__":
    """Records flow rate and tidal volume measured by a Senserion SFM3300 flow
    sensor attached to an Olimex ESP32-PoE-ISO board broadcasted over a serial
    connection.  It's helpful to use the Arduino IDE's Serial Plotter to see
    which serial port data will come over as weall as to verify that data is,
    in fact, coming over.

    The expected format of the incoming data is
    `SLMx10:%f.2\tTidalVol:%f.2\r\n`

    And the format of the outgoing data is
    `%f\tSLMx10:%f.2\tTidalVol:%f.2\n`
    with the first number being the floating-point milliseconds since Epoch.
    This data is saved to a file named with the starting date/time written
    per ISO 8601.
    """


    flow_serial_port = "/dev/cu.usbserial-1410"  # find port using Arduino IDE
    flow_sensor = serial.Serial(flow_serial_port, baudrate=115200)
    start_date_time = datetime.utcnow().strftime("%Y%m%dT%H%MZ")
    data_log = open(start_date_time + ".txt", "w+")

    try:
        print("Serial Port Relay and Logger")
        print("Program started and running.  CTL-C to terminate.")
        print(start_date_time)
        while True:
            try:
                raw_datum = flow_sensor.readline()
                millis_since_epoch = datetime.utcnow().timestamp() * 1000.0
                decoded_datum = "\t" + raw_datum.decode("ASCII")
                decoded_datum = decoded_datum.replace("\r\n", "")
                data_log.write(str(millis_since_epoch))
                data_log.write(decoded_datum)
                data_log.write("\n")
                print(decoded_datum)
            except UnicodeDecodeError:
                pass
    except KeyboardInterrupt:
        data_log.close()
        print("stopped")
        pass