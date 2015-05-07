from nose.tools import *
import primes.visualisation.generic as generic_
import primes.generator.prime as prime


class TestClass():
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_generic_constructor(self):
        settings = {"min": 0, "max": 2,
                    "width": 10, "height": 10}
        generic = generic_.Generic(prime.Generator, settings)
        assert_equals(generic.width, 10)
        assert_equals(generic.height, 10)
        assert_equals(generic.limit, 2)
        assert_true(hasattr(generic.generator, "minimum"))
        assert_equals(generic.settings, settings)
