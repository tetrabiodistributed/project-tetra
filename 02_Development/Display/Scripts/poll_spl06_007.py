from spl06_007 import PressureSensor, Calibrator, Communicator


if "__main__" == __name__:
    print("--Initialization")
    comms = Communicator(dump_communication=True)
    print("--Set Op Mode")
    comms.set_op_mode(PressureSensor.OpMode.command)
    print("--Set Pressure Sampling")
    comms.set_pressure_sampling()
    print("--Set Temperature Sampling")
    comms.set_temperature_sampling()
    # print(comms.calibration_coefficients)
    calibrator = Calibrator(comms.calibration_coefficients,
                            comms.pressure_scale_factor,
                            comms.temperature_scale_factor)
    # time.sleep(0.151)
    running = True
    while running:
        try:
            print("--Get Pressure")
            raw_pressure = comms.raw_pressure()
            print("--Get Temperature")
            raw_temperature = comms.raw_temperature()
            pressure = calibrator.pressure(raw_pressure, raw_temperature)
            temperature = calibrator.temperature(raw_temperature)
            # print(f"pressure: {pressure}\ttemperature: {temperature}\n"
            #       f"raw pressure: {raw_pressure}\t\t"
            #       f"raw temperature: {raw_temperature}\n")
            time.sleep(1.0)
            break
        except KeyboardInterrupt:
            running = False
            comms.close()
