from datetime import datetime
import matplotlib.pyplot as plt

from ProcessSampleData import ProcessSampleData

sensirion_data = ProcessSampleData("20200609T2050Z_sensirionFlowData.txt")
patrick_data = ProcessSampleData("20200609T2358Z_patrickData.txt")

sensirion_data_figure = plt.figure(0)
sensirion_data_figure.suptitle("Sensirion Data")
sensirion_flow_rate_subplot = sensirion_data_figure.add_subplot(211)
sensirion_flow_rate_subplot.set_ylabel("Flow Rate [mL/s]")
sensirion_flow_rate_subplot.plot(sensirion_data.relative_timestamps,
                                 sensirion_data.flow_rates)
sensirion_tidal_volume_subplot = sensirion_data_figure.add_subplot(212)
sensirion_tidal_volume_subplot.set_xlabel("Time [ms]")
sensirion_tidal_volume_subplot.set_ylabel("Tidal Volume [mL]")
sensirion_tidal_volume_subplot.plot(sensirion_data.relative_timestamps,
                                    sensirion_data.tidal_volumes)

patrick_data_figure = plt.figure(1)
patrick_data_figure.suptitle("Patrick's Data")
patrick_flow_rate_subplot = patrick_data_figure.add_subplot(311)
patrick_flow_rate_subplot.set_ylabel("Flow Rate [mL/s]")
patrick_flow_rate_subplot.plot(patrick_data.relative_timestamps,
       		                   patrick_data.flow_rates)
patrick_tidal_volume_subplot = patrick_data_figure.add_subplot(312)
patrick_tidal_volume_subplot.set_ylabel("Tidal Volume [mL]")
patrick_tidal_volume_subplot.plot(patrick_data.relative_timestamps,
                                  patrick_data.tidal_volumes)
patrick_pressure_subplot = patrick_data_figure.add_subplot(313)
patrick_pressure_subplot.set_xlabel("Time [ms]")
patrick_pressure_subplot.set_ylabel("Pressure [cmH2O]")
patrick_pressure_subplot.plot(patrick_data.relative_timestamps,
                              patrick_data.pressures)

try:
    plt.show()
except KeyboardInterrupt:
    sensirion_data_figure.savefig(datetime.utcnow().strftime("%Y%m%dT%H%MZ")
                                  + "_sensirionFlowData"
                                  + ".png")
    patrick_data_figure.savefig(datetime.utcnow().strftime("%Y%m%dT%H%MZ")
                                + "_patrickData"
                                + ".png")
    del(sensirion_data)
    del(patrick_data)