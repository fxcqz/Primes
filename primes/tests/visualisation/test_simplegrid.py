from nose.tools import *
import primes.visualisation.simplegrid.simplegrid as simplegrid
import primes.generator.prime as prime


class TestClass():
    def setUp(self):
        settings = {"min": 0, "max": 110,
                    "width": 10, "height": 10,
                    "bgcolour": (255, 255, 255, 255),
                    "fgcolour": (  0,   0,   0, 255)}
        self.v = simplegrid.SimpleGrid(prime.Generator, settings)
        self.v.generator.path = "./data/"

    def tearDown(self):
        pass

    def test_constructor(self):
        assert_equals(list(self.v.output), [])

    def test_generate(self):
        self.v.generate()
        assert_equals(self.v.output[0], (1, 0, 2))
        assert_equals(self.v.output[-1], (9, 9, 109))
