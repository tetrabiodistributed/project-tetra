import random


class PatientTubingDescriptorCalculator():
    """Takes in pressure and flow data from a sensor attached to a
    ventillator patient's airway and returns useful descriptors for
    medical staff to monitor.  Namely, inspiratory pressure, tidal
    volume, positive end-expiratory pressure (PEEP), peak inspiratory
    pressure (PIP), mean airway pressure (averaged over 60 seconds),
    and flow rate.

    Presently this is implemented with dummy values for the sake of
    testing.
    """


    def __init__(self):

        pass

    def add_flow_rate_datum(self, datum):
        """Adds a flow rate measurement to the internal buffer."""

        pass

    def add_pressure_datum(self, datum):
        """Adds a pressure measurement to the internal buffer."""

        pass

    @property
    def inspiratory_pressure(self):

        return random.uniform(5, 40)
        # return self._inspiratory_pressure

    @property
    def tidal_volume(self):

        return random.uniform(0, 5000)
        # return self._tidal_volume

    @property
    def PEEP(self):
        """Positive End-Expiratory Pressure"""

        return random.uniform(5, 10)
        # return self._PEEP

    @property
    def PIP(self):
        """Peak Insirpatory Pressure"""

        return random.uniform(20, 40)
        # return self._PIP

    @property
    def mean_airway_pressure(self):
        """The average pressure over the last 60 seconds"""

        return random.uniform(5, 40)
        # return self._mean_airway_pressure

    @property
    def flow_rate(self):

        return random.uniform(-0.25, 0.25)
        # return self._flow_rate
    
    
    @property
    def descriptors(self):
        """A dictionary of 
        - "Inspiratory Pressure"
        - "Tidal Volume"
        - "PEEP"
        - "PIP"
        - "Mean Airway Pressure"
        - "Flow Rate"
        """

        return {"Inspiratory Pressure": self.inspiratory_pressure,
                "Tidal Volume": self.tidal_volume,
                "PEEP": self.PEEP,
                "PIP": self.PIP,
                "Mean Airway Pressure": self.mean_airway_pressure,
                "Flow Rate": self.flow_rate}
                