from nose.tools import *
import os
import primes.generator.pairs as pairs


class TestClass():
    def setUp(self):
        self.gen = pairs.Generator(maximum=20)

    def tearDown(self):
        os.remove("primes/generator/data/primes/1.dat")
        os.removedirs("primes/generator/data/primes")
        if os.path.exists("primes/generator/data/pairs/2/1.dat"):
            os.remove("primes/generator/data/pairs/2/1.dat")
            os.removedirs("primes/generator/data/pairs/2")

    def test_pairs_constructor(self):
        assert_equals(self.gen.path, ("primes/generator/data/pairs/"))
        assert_equals(self.gen.gap, 2)
        assert_equals(self.gen.threshold, 500)

    def test_set_gap(self):
        self.gen.set_gap(4)
        assert_equals(self.gen.gap, 4)

    def test_set_specifics(self):
        self.gen.set_specifics({"gap": 6})
        assert_equals(self.gen.gap, 6)

    def test_pairs_generate(self):
        self.gen.generate()
        assert_equals(len(self.gen.data), 4)
        assert_equals(self.gen.data[0], 5)
        assert_true(13 in self.gen.data)
