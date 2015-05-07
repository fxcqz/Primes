from nose.tools import *
import primes.visualisation.cloud.cloud as cloud
import primes.generator.prime as prime


class TestClass():
    def setUp(self):
        settings = {"min": 0, "max": 110,
                    "width": 10, "height": 10,
                    "bgcolour": (255, 255, 255, 255),
                    "fgcolour": (  0,   0,   0, 255)}
        self.v = cloud.PrimeCloud(prime.Generator, settings)
        self.v.generator.path = "./data/"

    def tearDown(self):
        pass

    def test_constructor(self):
        assert_equals(self.v.current_x, 5)
        assert_equals(self.v.current_y, 5)
        assert_equals(self.v.mod, 11)

    def test_set_specifics(self):
        assert_equals(self.v.mod, 11)
        self.v.set_specifics({"mod": 5})
        assert_equals(self.v.mod, 5)

    def test_bound_check(self):
        self.v.current_x = -1
        self.v.bound_check()
        assert_equals(self.v.current_x, self.v.width-1)
        self.v.current_x = 11
        self.v.bound_check()
        assert_equals(self.v.current_x, 0)
        self.v.current_y = -1
        self.v.bound_check()
        assert_equals(self.v.current_y, self.v.height-1)
        self.v.current_y = 11
        self.v.bound_check()
        assert_equals(self.v.current_y, 0)

    def test_next_point(self):
        cy = self.v.current_y
        self.v.next_point(1)
        assert_equals(self.v.current_y, cy - 1)
        cx = self.v.current_x
        self.v.next_point(4)
        assert_equals(self.v.current_x, cx - 1)

    def test_generate(self):
        assert_equals(list(self.v.output), [])
        self.v.generate()
        assert_equals(self.v.output[5][5], 5000000)
