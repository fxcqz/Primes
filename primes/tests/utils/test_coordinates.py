from nose.tools import *
from primes.utils.coordinates import *


def test_pol_to_cart():
    assert_equals(pol_to_cart(1, 0), (1, 0))

def test_complex_to_real_2d():
    assert_equals(complex_to_real_2d(complex(3, 4)), (3, 4))

def test_real_to_complex_2d():
    assert_equals(real_to_complex_2d(3, 4), complex(3, 4))
