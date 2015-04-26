import numpy
import itertools
from numpy.polynomial.polynomial import polyfromroots, polyval


def poly_vals_in_range(minimum, maximum, roots):
    """Return a list of all results of a given polynomial within a range
    based on the roots of the polynomial itself.

    These roots will be selected by a user from the GUI.

    Arguments:
        minimum -- the lowest value in the dataset
        maximum -- the highest value in the dataset
        points -- the roots of the polynomial
    """
    poly = polyfromroots(roots)
    vals = itertools.takewhile(lambda x: x <= maximum,
                [polyval(y, poly) for y in range(minimum, maximum + 1)])
    vals = sorted(filter(lambda x: minimum <= x <= maximum, vals))
    return vals
