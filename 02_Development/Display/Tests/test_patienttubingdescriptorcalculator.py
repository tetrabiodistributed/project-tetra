import unittest

import numpy as np

from patienttubingdescriptorcalculator \
    import PatientTubingDescriptorCalculator


class TestPatientTubingDescriptorCalculator(unittest.TestCase):

    def setUp(self):
        self._calculator = PatientTubingDescriptorCalculator(0)

    def test_calculates_tidal_volume(self):
        dt = 0.01
        t = np.arange(0, 2, dt)
        to_process_data = np.sin(t)
        desired_processed_data = -np.cos(t)
        processed_data = np.array([desired_processed_data[0]])

        self._calculator.add_tidal_volume_value(processed_data[0])
        for i in range(1, len(t)):
            self._calculator.add_flow_rate_datum(to_process_data[i], t[i])
            processed_data = np.append(
                processed_data, self._calculator.descriptors["Tidal Volume"])
        rms_error = (
            np.sqrt(np.mean((desired_processed_data-processed_data)**2)))
        self.assertLess(rms_error, 0.05,
                        "Fails to integrate a Sin[t] flow rate to "
                        "-Cos[t] tidal volume.")
