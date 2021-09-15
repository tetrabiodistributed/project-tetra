import numpy as np
from numpy_ringbuffer import RingBuffer


class MovingAverageFilter(RingBuffer):
    """A moving average filter for an incoming stream of data.  Used
    like so:

        from moving_average_filter import MovingAverageFilter

        bufferSize = 4
        filter = MovingAverageFilter(bufferSize, default_value=0)
        filtered_data = []

        for datum in data:
            filter.append(datum)
            filtered_data.append(filter.get_datum())

        print(filtered_data)
    """

    def __init__(self, size, default_value=0):
        """Creates a filter instance.

        Parameters
        ----------
        size: int > 0
            The length of the buffer the moving average is performed
            over.  A long buffer will filter more noise than a short
            buffer, but will also introduce lag.
        default_value=0: float
            The filter will pad the the buffer with default_value when
            len(self) < size.
        """
        if size < 1:
            raise ValueError("Buffer size cannot be non-positive.")

        super().__init__(size)
        self._default_value = default_value

    def get_datum(self):
        """Returns the mean of the buffered values."""

        padding = np.array([self._default_value
                            for _ in range(self.maxlen - len(self))])
        return np.mean(np.append(self, padding))
