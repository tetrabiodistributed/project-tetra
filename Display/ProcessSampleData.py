from datetime import datetime
import pytz
from pytz import timezone, common_timezones


class ProcessSampleData():
    """Parses a file with flow rate, tidal volume, and optionally
    pressure data.  The expected formats are 

    `%f\tSLMx10:%f.2\tTidalVol:%f.2\n`
    with the first number being the floating-point milliseconds since
    Epoch, the second being ten times the flow rate in mL/s, and the
    last being the tidal volume in mL, and

    `%H:%M:%S.%f -> SLMx10:%f.2\tTidalVol:%f.2\tPressurex10:%f.2`
    with the first 11 character representing the time the datum was
    recorded as if on a digital clock (assuming the date as 2020-06-09
    and timezone as US/Pacific), the %f.2 after `SLMx10:` representing
    ten times the flow rate, the following %f.2 representing the tidal
    volume, and the last representing ten times the pressure.
    """


    def __init__(self, path_to_data):

        self._flow_data_file = open(path_to_data, "r")
        self._parseData()

    def __del__(self):

        self._flow_data_file.close()
        del(self._timestamps)
        del(self._flow_rates)
        del(self._tidal_volumes)

    def __len__(self):

        return len(self.timestamps)

    @property
    def timestamps(self):
        """Gives the list of timestamps data were taken at in
        milliseconds since Epoch
        """

        return self._timestamps

    @property
    def relative_timestamps(self):
        """Gives the list of timestamps data were taken at in
        milliseconds since the first data point
        """

        return [ timestamp - self.timestamps[0]
                 for timestamp in self.timestamps ]
    

    @property
    def flow_rates(self):
        """Gives the list of flow rates in mL/s"""

        return self._flow_rates
    
    @property
    def tidal_volumes(self):
        """Gives the list of tidal volumes in mL"""

        return self._tidal_volumes

    @property
    def pressures(self):
        """Gives the list of pressures in cmH2O"""

        return self._pressures
    

    def _parseData(self):

        self._timestamps = []
        self._flow_rates = []
        self._tidal_volumes = []
        self._pressures = []
        FLOW_RATE_MARKER = "SLMx10:"
        TIDAL_VOLUME_MARKER = "TidalVol:"
        PRESSURE_MARKER = "Pressurex10:"

        for datum in self._flow_data_file:
            splitDatum = datum.replace(" -> ", "\t").split("\t")
            try:
                self._timestamps.append(float(splitDatum[0]))
            except ValueError:
                self._timestamps \
                     .append(timezone("US/Pacific")
                             .localize(datetime
                                       .strptime(splitDatum[0],
                                                 "%H:%M:%S.%f")
                                       .replace(year=2020,
                                               month=6,
                                               day=9))
                             .astimezone(pytz.utc)
                             .timestamp() * 1000.0)

            self._flow_rates.append(float(splitDatum[1]
                                          .replace(FLOW_RATE_MARKER,
                                                   "")
                                          .strip("\n")) / 10)
            self._tidal_volumes.append(float(splitDatum[2]
                                             .replace(TIDAL_VOLUME_MARKER,     "")
                                             .strip("\n")))

            if (PRESSURE_MARKER in datum):
                self._pressures.append(float(splitDatum[3]
                                             .replace(PRESSURE_MARKER,
                                                      "")
                                             .strip("\n")) / 10)