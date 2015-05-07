from nose.tools import *
import os
import primes.utils.gl_pixdata as pd


class TestClass():
    def setUp(self):
        pass

    def tearDown(self):
        os.remove("img.png")

    def test_pixels_to_image(self):
        pixels = [[(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0)],
                  [(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0)],
                  [(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0)],
                  [(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0)]]
        size = (4, 4)
        path = "./img.png"
        pd.pixels_to_image(pixels, size, path)
        assert_true(os.path.exists("./img.png"))
