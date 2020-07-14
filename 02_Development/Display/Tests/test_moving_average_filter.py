import unittest

from moving_average_filter import MovingAverageFilter


class TestMovingAverageFilter(unittest.TestCase):

    def setUp(self):
        self._buffer_size = 4
        self._filter = MovingAverageFilter(self._buffer_size)

    def test_get_datum_constant_series(self):
        for _ in range(self._buffer_size):
            self._filter.append(1.0)

        self.assertAlmostEqual(self._filter.get_datum(), 1.0,
                               msg="Fails to calculate the mean of a "
                               "constant series.")

    def test_get_datum_increasing_series(self):
        for i in range(self._buffer_size):
            self._filter.append(i)

        self.assertAlmostEqual(self._filter.get_datum(), 1.5,
                               msg="Fails to calculate the mean of a "
                               "constant series.")

    def test_get_datum_empty_buffer(self):
        self.assertAlmostEqual(self._filter.get_datum(), 0.0,
                               msg="Fails to return a default value for an "
                               "empty buffer.")

    def test_get_datum_party_full_buffer(self):
        self._filter.append(4)

        self.assertAlmostEqual(self._filter.get_datum(), 1.0,
                               msg="Fails to pad the buffer with zeros "
                               "when it's only partly filled with data.")

    def test_illgally_sized_buffer(self):
        with self.assertRaises(ValueError,
                               msg="Fails to raise an error when the "
                               "buffer size is set to 0."):
            MovingAverageFilter(0)

        with self.assertRaises(ValueError,
                               msg="Fails to raise an error when the "
                               "buffer size is set to negative."):
            MovingAverageFilter(-1)
