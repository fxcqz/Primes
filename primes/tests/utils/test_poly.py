from nose.tools import *
import primes.utils.poly as poly


def test_poly_vals_in_range():
    minimum = 0
    maximum = 100
    roots = [2, 3, 5]
    assert_equals(list(poly.poly_vals_in_range(minimum, maximum, roots)),
                  [0, 0, 0, 12, 40, 90])
