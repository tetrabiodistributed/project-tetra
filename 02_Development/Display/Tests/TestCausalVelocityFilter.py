import math
import numpy as np
import unittest
import matplotlib.pyplot as plt

from CausalVelocityFilter import CausalVelocityFilter


class TestCausalVelocityFilter(unittest.TestCase):


    def testInit_nominal(self):

        velocity_filter = CausalVelocityFilter(100)
        self.assertIsNotNone(filter,
                             "Fails to initialize a velocity filter")

    def test_differentiates(self):

        dt = 0.001
        t = np.arange(0, 10, dt)
        velocity_filter = CausalVelocityFilter(100)
        to_filter_data = np.sin(t)
        filtered_data = np.array([])
        desired_filtered_data = np.cos(t)
        error = np.array([])
        for i in range(len(to_filter_data)):
            velocity_filter.append(to_filter_data[i], dt)
            filtered_data = np.append(filtered_data, velocity_filter.get_datum())
            error = np.append(error, desired_filtered_data[i] - filtered_data[i])
        rms_error = np.sqrt(np.mean(error**2))
        self.assertLess(rms_error, 0.1,
                        "Fails to differentiate a data series "
                        + "approximating sin(x) within <0.1 rms error")

    def test_rejectsHighFrequency(self):

        dt = 0.001
        t = np.arange(0, 10, dt)
        velocity_filter = CausalVelocityFilter(70)
        to_filter_data = np.sin(t) + 0.001*np.sin(100*t)
        filtered_data = np.array([])
        desired_filtered_data = np.cos(np.arange(0, 10, dt))
        error = np.array([])
        for i in range(len(to_filter_data)):
            velocity_filter.append(to_filter_data[i], dt)
            filtered_data = np.append(filtered_data, velocity_filter.get_datum())
            error = np.append(error, desired_filtered_data[i] - filtered_data[i])
        rms_error = np.sqrt(np.mean([err**2 for err in error]))
        self.assertLess(rms_error, 0.05,
                        "Fails to differentiate a data series while "
                        + "rejecting high-frequency noise within "
                        + "<0.01 rms error")