import numpy as np
from numpy_ringbuffer import RingBuffer


class CausalVelocityFilter():
    """Calculates the derivative of data that's appended to the
    internal buffer and allows you to get a moving average of the
    derivative with window size defined by the init.
    """


    def __init__(self, windowSize):
        """Initializes self.
        windowSize defines the width of the moving average buffer.
        Too narrow and it doesn't do much filtering, too wide and it
        lags behind the acutal derivative
        """

        self._derivativeBuffer = RingBuffer(windowSize)
        self._previousDatum = 0.0

    def get_datum(self):
        """Get the present rate of change of the incomimg data"""

        return np.mean(self._derivativeBuffer)

    def append(self, datum, timeElapsed):
        """Add a measurement and an elapsed time to the filter's
        internal buffer to be able to find the rate of change.
        """

        self._derivativeBuffer.append((datum - self._previousDatum)
                                      / timeElapsed)
        self._previousDatum = datum