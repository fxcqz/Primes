from nose.tools import *
import primes.visualisation.gl_base as gl_base


class TestClass():
    def setUp(self):
        self.c = gl_base.Canvas(limit=9,bgcolour=(255,255,255,255),fgcolour=(0,0,0,255),
                    data=[2,3,5,7], size=(10,10))

    def tearDown(self):
        pass

    def test_mg(self):
        grid = gl_base.mg(9)
        assert_equals(list(grid['position'][0]), [0., 0., 0.])
        assert_equals(list(grid['position'][-1]), [2., 2., 0.])
        assert_equals(list(grid['colour'][0]), [1, 0, 0, 1])
        assert_equals(list(grid['colour'][-1]), [1, 0, 0, 1])
        assert_equals(grid['toggled'][0], 0.)
        assert_equals(grid['highlighted'][0], 0.)

    def test_zoom(self):
        size = 10
        resolution = 2
        gl_z = 5
        step = 1
        assert_equals(gl_base.zoom(size, resolution, gl_z, step), 50/6.)

    def test_norm_colour(self):
        colour = (255, 255, 255)
        assert_equals(gl_base.norm_colour(colour), (1., 1., 1., 1.))

    def test_canvas_constructor(self):
        assert_equals(list(self.c.data), [2,3,5,7])
        assert_equals(self.c.bgcolour, (1.,1.,1.,1.))
        assert_equals(self.c.fgcolour, (0.,0.,0.,1.))
        assert_equals(self.c.limit, 9)
        assert_equals(self.c.size, (10,10))

    def test_get_selection_colours(self):
        colours = self.c.get_selection_colours()
        assert_equals(colours['toggled'], (0.5, 0.5, 0.5, 1.))
        assert_equals(colours['highlighted'], (0.25, 0.25, 0.25, 1.))

    def test_set_limit(self):
        self.c.set_limit(16)
        assert_equals(self.c.limit, 16)

    def test_set_colour(self):
        assert_equals(list(self.c.grid['colour'][0]), [1, 1, 1, 1])
        self.c.set_colour((0,1,0), self.c.grid, (0, 0))
        assert_equals(list(self.c.grid['colour'][-3]), [0, 1, 0, 1])

    def test_coord_to_index(self):
        x, y = 1, 1
        assert_equals(self.c.coord_to_index(x, y), 4)
