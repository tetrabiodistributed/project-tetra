import unittest

import numpy as np

from causal_integral_filter import CausalIntegralFilter


class TestCausalIntegralFilter(unittest.TestCase):

    def test_constant_zero_data(self):
        dt = 0.01
        t = np.arange(0, 2, dt)
        to_process_data = 0*t
        desired_processed_data = 0*t
        processed_data = np.array([desired_processed_data[0]])

        filter = CausalIntegralFilter(processed_data[0], t[0])
        for i in range(1, len(t)):
            filter.append(to_process_data[i], t[i])
            processed_data = np.append(processed_data, filter.get_datum())
        rms_error = (
            np.sqrt(np.mean((desired_processed_data-processed_data)**2)))
        self.assertLess(rms_error, 0.05,
                        "Fails to integrate a constant 0 signal to 0.")

    def test_constant_one_data(self):
        dt = 0.01
        t = np.arange(0, 2, dt)
        to_process_data = 0*t + 1
        desired_processed_data = t + 1
        processed_data = np.array([desired_processed_data[0]])

        filter = CausalIntegralFilter(processed_data[0], t[0])
        for i in range(1, len(t)):
            filter.append(to_process_data[i], t[i])
            processed_data = np.append(processed_data, filter.get_datum())
        rms_error = (
            np.sqrt(np.mean((desired_processed_data-processed_data)**2)))
        self.assertLess(rms_error, 0.05,
                        "Fails to integrate a constant 1 signal to t+1.")

    def test_linear_data(self):
        dt = 0.01
        t = np.arange(0, 2, dt)
        to_process_data = t
        desired_processed_data = 0.5*t**2
        processed_data = np.array([desired_processed_data[0]])

        filter = CausalIntegralFilter(processed_data[0], t[0])
        for i in range(1, len(t)):
            filter.append(to_process_data[i], t[i])
            processed_data = np.append(processed_data, filter.get_datum())
        rms_error = (
            np.sqrt(np.mean((desired_processed_data-processed_data)**2)))
        self.assertLess(rms_error, 0.05,
                        "Fails to integrate a t signal to 1/2 t^2.")

    def test_sine_data(self):
        dt = 0.01
        t = np.arange(0, 2, dt)
        to_process_data = np.sin(t)
        desired_processed_data = -np.cos(t)
        processed_data = np.array([desired_processed_data[0]])

        filter = CausalIntegralFilter(processed_data[0], t[0])
        for i in range(1, len(t)):
            filter.append(to_process_data[i], t[i])
            processed_data = np.append(processed_data, filter.get_datum())
        rms_error = (
            np.sqrt(np.mean((desired_processed_data-processed_data)**2)))
        self.assertLess(rms_error, 0.05,
                        "Fails to integrate a Sin[t] signal to -Cos[t].")
