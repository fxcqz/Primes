__author__ = 'Matt'
import numpy as np


def pol_to_cart(rho, phi):
    # http://stackoverflow.com/questions/20924085/python-conversion-between-coordinates
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return x, y


def complex_to_real_2d(z):
    x = np.real(z)
    y = np.imag(z)
    return x, y


def real_to_complex_2d(x, y):
    return np.complex(x, y)