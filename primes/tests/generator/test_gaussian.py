from nose.tools import *
import os
import primes.generator.gaussian as gaussian


class TestClass():
    def setUp(self):
        self.gen = gaussian.Generator(minimum=complex(-5, -5), maximum=complex(5, 5))

    def tearDown(self):
        os.remove("primes/generator/data/primes/1.dat")
        os.removedirs("primes/generator/data/primes")
        if os.path.exists("primes/generator/data/gaussians/1.dat"):
            os.remove("primes/generator/data/gaussians/1.dat")
            os.removedirs("primes/generator/data/gaussians")

    def test_gaussian_constructor(self):
        assert_equals(self.gen.path, "primes/generator/data/gaussians/")
        assert_equals(self.gen.datatype, complex)
        assert_equals(self.gen.threshold, 300)
        assert_equals(list(self.gen.primes), [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47])

    def test_is_gaussian_prime(self):
        assert_false(self.gen.is_gaussian_prime(complex(0, 0)))
        assert_true(self.gen.is_gaussian_prime(complex(-5, -4)))

    def test_gaussian_generate(self):
        self.gen.generate()
        assert_equals(len(self.gen.data), 40)
        assert_true(complex(-5, -4) in self.gen.data)
