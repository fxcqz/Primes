from nose.tools import *
import primes.utils.handles as handles


def test_handles():
    assert_true(isinstance(handles.generators['Primes'], object))
    assert_true(isinstance(handles.visualisations['Wireframe'], object))
    assert_true(hasattr(handles.generators['Gaussians'], "Generator"))
    assert_false(hasattr(handles.visualisations['Ulam Spiral'], "Foolam Spiral"))
