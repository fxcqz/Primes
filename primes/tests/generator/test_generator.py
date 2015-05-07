from nose.tools import *
import os
import primes.generator.generator as generator


class TestClass():
    def setUp(self):
        self.gen = generator.Generator()
        self.gen.path = "./data/"

    def tearDown(self):
        if os.path.exists("data/2.dat"):
            os.remove("data/2.dat")
        if os.path.exists("data/3.dat"):
            os.remove("data/3.dat")

    def test_constructor(self):
        assert_is_not_none(self.gen)
        assert_equals(self.gen.minimum, 0)
        assert_equals(self.gen.maximum, 1)
        assert_equals(self.gen.data, [])

    def test_data_files_from_dir(self):
        assert_equals(self.gen.data_files_from_dir(), ['1.dat'])

    def test_read_cache(self):
        self.gen.maximum = 10
        data = self.gen.read_cache()
        assert_equals(list(data), [2,3,5,7])

    def test_complex_range(self):
        r = self.gen.complex_range(complex(-5, -5), complex(5, 5))
        assert_equals(len(r), 100)
        assert_equals(r[0], complex(-5, -5))
        assert_equals(r[-1], complex(4, 4))

    def test_not_in_cache(self):
        g = generator.Generator(maximum=10)
        g.path = "./data/"
        g.data = g.read_cache()
        assert_equals(g.not_in_cache(), ([0, 1], [8, 9, 10]))

    def test_complex_not_in_cache(self):
        g = generator.Generator(complex(-2, -2), complex(2, 2))
        g.path = "./data/"
        g.datatype = complex
        g.data = [complex(0, 0)]
        assert_equals(g.not_in_cache(), ([complex(-2, -2), complex(-2, -1), complex(-1, -2), complex(-1, -1)],
                                         [complex( 1,  1), complex( 1,  2), complex( 2,  1), complex( 2,  2)]))

    def test_next_filename(self):
        assert_equals(self.gen.next_filename("./data/"), "2.dat")
