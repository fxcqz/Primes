import numpy as np


"""Utility functions for conversions between various coordinate systems."""

def pol_to_cart(rho, phi):
    """Converts Polar Coordinates to Cartesian Coordinates.

    See:
        http://stackoverflow.com/questions/20924085/python-conversion-between-coordinates

    Arguments:
        rho -- displacement component of the polar coordinate.
        phi -- angle component of the polar coordinate.
    """
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return x, y


def complex_to_real_2d(z):
    """Converts a complex number to a position in 2d Cartesian space.
    
    Arguments:
        z -- a complex number
    """
    if not isinstance(z, complex):
        return
    x = np.real(z)
    y = np.imag(z)
    return x, y


def real_to_complex_2d(x, y):
    """Converts a position in 2d Cartesian space to a complex number.

    Arguments:
        x -- the x component (maps to the real axis)
        y -- the y component (maps to the imaginary axis)
    """
    return np.complex(x, y)
