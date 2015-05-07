from nose.tools import *
import os
import primes.generator.prime as prime


class TestClass():
    def setUp(self):
        self.gen = prime.Generator()

    def tearDown(self):
        if os.path.exists("data/2.dat"):
            os.remove("data/2.dat")

    def test_prime_constructor(self):
        assert_equals(self.gen.path, "primes/generator/data/primes/")

    def test_j_increment(self):
        self.gen.maximum = 10
        assert_equals(self.gen.j_increment(1), range(1, 11))
        assert_equals(self.gen.j_increment(5), [])

    def test_prime_generate(self):
        self.gen.maximum = 10
        self.gen.path = "./data/"
        self.gen.generate()
        assert_equals(list(self.gen.data), [2, 3, 5, 7])

    def test_prime_big_generate(self):
        self.gen.path = "./data/"
        self.gen.maximum = 100000
        self.gen.generate()
        assert_equals(self.gen.data[-1], 99991)
