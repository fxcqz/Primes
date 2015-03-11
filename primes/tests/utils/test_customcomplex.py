from nose.tools import *
from primes.utils.custom_complex import CustomComplex
import numpy


def test_complex_init():
    # 2 ways of instantiating custom complex
    a = CustomComplex(2, 3)
    assert_equals(numpy.real(a), 2)
    assert_equals(numpy.imag(a), 3)
    b = CustomComplex(complex(1, 2))
    assert_equals(numpy.real(b), 1)
    assert_equals(numpy.imag(b), 2)

def test_cc_eq():
    assert_true(CustomComplex(0, 0) == CustomComplex(0, 0))
    assert_false(CustomComplex(1, 0) == CustomComplex(0, 1))
    assert_false(CustomComplex(0, 0) == CustomComplex(1, 1))

def test_cc_lt():
    assert_true(CustomComplex(0, 0) < CustomComplex(1, 1))
    assert_false(CustomComplex(1, 1) < CustomComplex(0, 0))

def test_cc_le():
    assert_true(CustomComplex(0, 0) <= CustomComplex(1, 1))
    assert_true(CustomComplex(1, 1) <= CustomComplex(1, 1))
    assert_false(CustomComplex(1, 1) <= CustomComplex(0, 0))

def test_cc_gt():
    assert_true(CustomComplex(1, 1) > CustomComplex(0, 0))
    assert_false(CustomComplex(0, 0) > CustomComplex(1, 1))
