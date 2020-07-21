import random

from numpy_ringbuffer import RingBuffer

from causal_integral_filter import CausalIntegralFilter


class PatientTubingDescriptorCalculator():

    def __init__(self, current_time):
        self._flow_rate_sample_times = RingBuffer(2)
        self._flow_rate_sample_times.append(current_time)

        self._tidal_volume_filter = CausalIntegralFilter(0, current_time)

    def add_flow_rate_datum(self, datum, current_time):
        self._tidal_volume_filter.append(datum, current_time)

    def add_pressure_datum(self, datum):
        pass

    def add_tidal_volume_value(self, tidal_volume):
        self._tidal_volume_filter.append_integral_value(tidal_volume)

    def _flow_rate(self):
        return random.uniform(-200, 200)

    def _inspiratory_pressure(self):
        return random.uniform(0, 25)

    def _PEEP(self):
        return random.uniform(2, 5)

    def _peak_pressure(self):
        return random.uniform(23, 25)

    def _tidal_volume(self):
        return self._tidal_volume_filter.get_datum()

    @property
    def descriptors(self):
        return {"Flow Rate": self._flow_rate(),
                "Inspiratory Pressure": self._inspiratory_pressure(),
                "PEEP": self._PEEP(),
                "Peak Pressure": self._peak_pressure(),
                "Tidal Volume": self._tidal_volume()}
