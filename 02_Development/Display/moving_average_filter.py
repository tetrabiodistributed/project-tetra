import numpy as np
from numpy_ringbuffer import Ringbuffer


class MovingAverageFilter(Ringbuffer):


	def __init__(self, size):

		super().__init__(size)

	def get_datum(self):

		return np.mean(self)