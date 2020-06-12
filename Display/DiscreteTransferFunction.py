import math
import numpy as np

from numpy_ringbuffer import RingBuffer


class DiscreteTransferFunction(RingBuffer):
    """Generates a single-input single-output transfer function that
    transforms data based on the given numerator and denominator
    coefficients.

    Add data to the internal buffer with
    DiscreteTransferFunction.append()

    This class is inspired by the Discrete Transfer Fcn in
    Matlab/Simulink.
    https://www.mathworks.com/help/simulink/slref/discretetransferfcn.html
    """

    def __init__(self, numerator, denominator):
        """Generates a transfer function such that the values in the
        lists numerator and denominator are the coefficients of a
        transfer function of the order of the length of the longer list
        where the first element of each list is on the highets order
        term.  For example,

        DiscreteTransferFunction([1, -1], [1, -1.85, 0.9])

        results in a transfer function of the form

              z - 1
        ------------------
        z^2 - 1.85 z + 0.9

        where z^n is the nth most recent value added to the buffer.
        """

        super().__init__(max(len(numerator)-1, len(denominator)-1))
        self._numerator = numerator
        self._denominator = denominator

    @property
    def numerator(self):
        """The coefficients of the numerator of the transfer function
        in order from highest order to lowest"""
        return self._numerator

    @property
    def denominator(self):
        """The coefficients of the denominator of the transfer function
        in order from highest order to lowest"""
        return self._denominator

    def get_datum(self):
        """Calculates the value of the transfer function given the
        contents of the buffer.
        """

        numerator = self._evaluate_polynomial_over_buffer(self._numerator)
        denominator = self._evaluate_polynomial_over_buffer(self._denominator)
        return numerator/denominator

    def _evaluate_polynomial_over_buffer(self, coefficients):

        return sum(coefficient * bufferValue
                   for (coefficient, bufferValue)
                   in zip(reversed(coefficients[:-1]), reversed(self))) \
               + coefficients[-1]

    def __str__(self):
        """Makes a polynomial representation of the transfer function.
        
        >>> print(DiscreteTransferFunction([1, -1], [1, -1.85, 0.9]))
              z - 1
        ------------------
        z^2 - 1.85 z + 0.9
        """

        numerator_string = self._z_polynomial(self._numerator)
        denominator_string = self._z_polynomial(self._denominator)

        fraction_bar = "-" * max(len(numerator_string),len(denominator_string))

        padding = " " * (abs(len(numerator_string)
                             - len(denominator_string)) // 2)
        if (len(numerator_string) > len(denominator_string)):
            denominator_string = padding + denominator_string
        else:
            numerator_string = padding + numerator_string

        return numerator_string + "\n" + fraction_bar + "\n" + denominator_string

    def _z_polynomial(self, coefficients):

        polynomial_string = ""
        for i in reversed(range(len(coefficients))):
            if (i + 1 == len(coefficients)):
                polynomial_string = polynomial_string \
                    + self._z_term(coefficients[-(i+1)], i)
                if math.isclose(coefficients[i], 1) and i != 0:
                    polynomial_string = polynomial_string[1:]
            else:
                polynomial_string = polynomial_string \
                    + (" + " if coefficients[-(i+1)] >= 0 else " - ") \
                    + self._z_term(abs(coefficients[-(i+1)]), i)

        return polynomial_string

    def _z_term(self, coefficient, degree):

        if degree == 0:
            return str(coefficient)
        else:
            coefficientString = "" if math.isclose(coefficient, 1) \
                                   else str(coefficient)
            if degree == 1:
                return coefficientString + " z"
            else:
                return coefficientString + " z^" + str(degree)