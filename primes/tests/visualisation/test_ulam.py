from nose.tools import *
import primes.visualisation.ulam.ulam as ulam
import primes.generator.prime as prime


class TestClass():
    def setUp(self):
        settings = {"min": 0, "max": 110,
                    "width": 10, "height": 10,
                    "bgcolour": (255, 255, 255, 255),
                    "colour": (0, 0, 0, 255)}
        self.u = ulam.UlamSpiral(prime.Generator, settings)
        self.u.generator.path = "./data/"

    def tearDown(self):
        pass

    def test_next_point(self):
        # dir 0
        assert_equals(self.u.current_y, int(self.u.height / 2))
        self.u.next_point()
        assert_equals(self.u.current_y, int(self.u.height / 2) + 1)
        # dir 1
        assert_equals(self.u.current_x, int(self.u.width / 2))
        self.u.direction = 1
        self.u.next_point()
        assert_equals(self.u.current_x, int(self.u.height / 2) - 1)
        # dir 2
        self.u.direction = 2
        self.u.next_point()
        assert_equals(self.u.current_y, int(self.u.height / 2))
        # dir 3
        self.u.direction = 3
        self.u.next_point()
        assert_equals(self.u.current_x, int(self.u.width / 2))

    def test_generate(self):
        assert_equals(len(self.u.output), 0)
        self.u.generate()
        assert_not_equals(len(self.u.output), 0)
        assert_equals(self.u.output[0], [5, 6, 2])
