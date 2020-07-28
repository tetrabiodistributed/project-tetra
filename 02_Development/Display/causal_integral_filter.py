from numpy_ringbuffer import RingBuffer


class CausalIntegralFilter():

    def __init__(self, initial_value, initial_time):
        self._y = initial_value
        self._t_buffer = RingBuffer(2)
        self._t_buffer.append(initial_time)

    def append_integral_value(self, y):
        self._y = y

    def append(self, dydt, t):
        self._t_buffer.append(t)
        self._y += dydt * (self._t_buffer[-1] - self._t_buffer[-2])

    def get_datum(self):
        return self._y
