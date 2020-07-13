import random


class PatientTubingDescriptorCalculator():


    def __init__(self):
        pass

    def add_flow_rate_datum(self, datum):
        pass

    def add_pressure_datum(self, datum):
        pass

    def _flow_rate(self):
        return random.uniform(-200, 200)

    def _inspiratory_pressure(self):
        return random.uniform(0, 25)

    def _PEEP(self):
        return random.uniform(2, 5)

    def _peak_pressure(self):
        return random.uniform(23, 25)

    def _tidal_volume(self):
        return random.uniform(0, 200)

    @property
    def descriptors(self):
        return {"Flow Rate": self._flow_rate(),
                "Inspiratory Pressure": self._inspiratory_pressure(),
                "PEEP": self._PEEP(),
                "Peak Pressure": self._peak_pressure(),
                "Tidal Volume": self._tidal_volume()}
