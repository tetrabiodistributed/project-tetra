import unittest
import math

from DiscreteTransferFunction import DiscreteTransferFunction


class TestDiscreteTransferFunction(unittest.TestCase):


    def testInit_nominal(self):

        tf = DiscreteTransferFunction([1], [1])
        self.assertIsNotNone(tf,
                             "Fails to initialize a discrete "
                             + "transfer function")

    def testInit_divideByZero(self):

        tf = DiscreteTransferFunction([1], [0])
        self.assertRaises(ZeroDivisionError)

    def testInit_divideByZeroMany(self):

        tf = DiscreteTransferFunction([1], [0] * 50)
        self.assertRaises(ZeroDivisionError)

    def testAppend_nominal(self):

        tf = DiscreteTransferFunction([1, 1], [1])
        tf.append(0)
        self.assertTrue(tf.is_full,
                        "Fails to append a datum to the transfer "
                        + "function's buffer")

    def testAppend_wrongDataType(self):

        tf = DiscreteTransferFunction([1], [1])
        tf.append("doesn't quack like a float")
        self.assertRaises(ValueError)

    def testAppend_manyData(self):

        tf = DiscreteTransferFunction([1, 1, 1, 1, 1], [1])
        tf.append(0)
        tf.append(1)
        tf.append(2)
        tf.append(3)
        tf.append(4)
        self.assertTrue(tf.is_full,
                        "Fails to append many data to the transfer "
                        + "function")

    def testGetDatum_nominal(self):

        tf = DiscreteTransferFunction([1], [1])
        tf.append(0)
        self.assertAlmostEqual(tf.get_datum(), 1,
                               msg="Fails to give the quotient of the "
                                   + "constant terms when the "
                                   + "numerator and denominator are "
                                   + "both length 1")

    def testGetDatum_firstOrderTerm(self):

        tf = DiscreteTransferFunction([1, 1], [1])
        tf.append(1)
        self.assertAlmostEqual(tf.get_datum(), 2,
                               msg="Fails to add a first order term "
                                   + "in the numerator")

    def testGetDatum_secondOrderTerm(self):
        
        tf = DiscreteTransferFunction([1, 1, 1], [1])
        tf.append(1)
        tf.append(1)
        self.assertAlmostEqual(tf.get_datum(), 3,
                               msg="Fails to add a second order term "
                                   + "in the numerator")

    def testGetDatum_underFilledBuffer(self):

        tf = DiscreteTransferFunction(list(reversed(range(10))), [1])
        tf.append(1)
        tf.append(2)
        self.assertAlmostEqual(tf.get_datum(), 4,
                               msg="Fails to return data using only "
                                   + "the lowest order coefficients")

    def testGetDatum_fibonacci(self):

        tf = DiscreteTransferFunction([1, 1, 0], [1])
        fibonacciNumbers = [1, 1]
        tf.append(1)
        tf.append(1)

        for _ in range(4):
            fibonacciNumbers.append(tf.get_datum())
            tf.append(tf.get_datum())

        desiredList = [1, 1, 2, 3, 5, 8]
        self.assertTrue(all(math.isclose(actual, desired)
                            for (actual, desired) in
                            zip(fibonacciNumbers, 
                                desiredList)),
                         "Fails to generate a sequence of numbers "
                         + "with the numerator having non-constant "
                         + "terms\n"
                         + "   " + str(desiredList) + "\n"
                         + "!= " + str(fibonacciNumbers))

    def testGetDatum_inverseFibonacci(self):
        """invereFibonacci(n) =
               1 / (inverseFibonacci(n-1) + inverseFibonacci(n-2))
        """

        tf = DiscreteTransferFunction([1], [1, 1, 0])
        inverseFibonacciNumbers = [1, 1]
        tf.append(1)
        tf.append(1)

        for _ in range(4):
            inverseFibonacciNumbers.append(tf.get_datum())
            tf.append(tf.get_datum())

        desiredList = [1, 1, 1/2, 2/3, 6/7, 21/32]
        self.assertTrue(all(math.isclose(actual, desired)
                            for (actual, desired) in
                            zip(inverseFibonacciNumbers, 
                                desiredList)),
                        "Fails to generate a sequence of numbers with "
                        + "the denominator having non-constant terms\n"
                        + "   " + str(desiredList) + "\n"
                        + "!= " + str(inverseFibonacciNumbers))

    def testGetDatum_regularAndInverseFibonacci(self):

        tf = DiscreteTransferFunction([1, 1, 0], [1, 1, 0])
        regularAndInverseFibonacciNumbers = [1, 1]
        tf.append(1)
        tf.append(1)

        for _ in range(4):
            regularAndInverseFibonacciNumbers.append(tf.get_datum())
            tf.append(tf.get_datum())

        desiredList = [1, 1, 1, 1, 1, 1]
        self.assertTrue(all(math.isclose(actual, desired)
                            for (actual, desired) in
                            zip(regularAndInverseFibonacciNumbers, 
                                desiredList)),
                        "Fails to generate a sequence of numbers with "
                        + "the numerator and denominator having "
                        + "non-constant terms\n"
                        + "   " + str(desiredList) + "\n"
                        + "!= " + str(regularAndInverseFibonacciNumbers))

    def testStr_nominal(self):

        tf = DiscreteTransferFunction([1, -1], [1, -1.85, 0.9])
        self.assertEqual(str(tf),   "       z - 1\n"
                                  + "-------------------\n"
                                  + " z^2 - 1.85 z + 0.9",
                         "Fails to represent a transfer function as a "
                         + "pretty string.")

    def testStr_leadingCoefficientOtherThanOne(self):

        tf = DiscreteTransferFunction([2, -2], [1, -0.8])
        self.assertEqual(str(tf),   "2 z - 2\n"
                                  + "--------\n"
                                  + " z - 0.8",
                         "Fails to properly format a transfer function "
                         + "that has a leading coefficient other than "
                         + "one")

    def testStr_leadingCoefficientsAreConstantTermsAndOne(self):

        tf = DiscreteTransferFunction([1], [1])
        self.assertEqual(str(tf),   "1\n"
                                  + "-\n"
                                  + "1",
                         "Fails to properly format a transfer function "
                         + "where the leading term is both constant "
                         + "and the coefficient is equal to 1")