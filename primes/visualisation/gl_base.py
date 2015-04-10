import sys
import numpy
from vispy import app, gloo
from vispy.util.transforms import perspective, translate


VERTEX = """
#version 120
attribute vec3 position;
attribute vec4 colour;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

uniform float size;
uniform vec2 pan;

varying vec4 v_colour;

void main() {
    v_colour = colour;
    gl_Position = projection * model * view * vec4(position + vec3(pan[0], pan[1], 0.0), 1.0);
    gl_PointSize = size;
}
"""

FRAGMENT = """
#version 120
varying vec4 v_colour;

void main() {
    gl_FragColor = v_colour;
}
"""

def mg(limit, colour=(1,0,0,1)):
    rows = int(numpy.ceil(limit ** 0.5))
    n = rows ** 2
    points = []
    for y in range(rows):
        for x in range(rows):
            points.append([float(x),float(y),0.])
    ret = numpy.zeros(n, dtype=[("position", 'f4', 3), ("colour", 'f4', 4)])
    ret["position"] = numpy.array(points)
    ret["colour"] = colour
    # maybe add a "toggled" array for marking points (selection)
    return ret

def zoom(size, resolution, gl_z, step):
    pix_z = gl_z * (resolution / 2.) # current
    new_z = (gl_z + step) * (resolution / 2.)
    ratio = pix_z / new_z
    return size * ratio

def norm_colour(colour):
    return (colour[0]/255., colour[1]/255., colour[2]/255., colour[3]/255.)

class Canvas(app.Canvas):
    def __init__(self, *args, **kwargs):
        # override canvas constructor to obtain a limit
        self.limit = kwargs.pop('limit', None)
        self.bgcolour = norm_colour(kwargs.pop('bgcolour', None))
        self.fgcolour = norm_colour(kwargs.pop('fgcolour', None))
        app.Canvas.__init__(self, *args, **kwargs)
        app.use_app('PyQt4')
        self.program = gloo.Program(VERTEX, FRAGMENT)
        if self.limit is None:
            # default to 1000 is no limit is specified
            self.limit = 1000
        if self.bgcolour is None:
            self.bgcolour = (1,1,1,1)
        if self.fgcolour is None:
            self.fgcolour = (0,0,0,1)
        self.init_pos = int(numpy.ceil(self.limit ** 0.5))
        self.grid = mg(self.limit, self.bgcolour)
        # gl/gloo buffers
        verts = gloo.VertexBuffer(self.grid['position'].copy())
        self.program['position'] = verts
        self.program['colour'] = gloo.VertexBuffer(self.grid['colour'].copy())
        # view (camera) matrices
        self.view = numpy.eye(4, dtype=numpy.float32)
        self.model = numpy.eye(4, dtype=numpy.float32)
        # the purpose of setting the near limit to 0.5 is that at any distance
        # nearer the points, the zooming stops working
        self.projection = perspective(135., self.size[0] /
                                      float(self.size[1]), 0.5, 500.)
        # initial camera position
        self.pan = self.program['pan'] = [0., 0.]
        # zoom data
        #   size: sent to glsl to be gl_PointSize
        #   resolution: initial [comparative] grid size
        #   gl_z: size of z-value from camera to origin (in gl coords)
        self.zoom = {"size": self.size[1] / float(self.init_pos),
                     "resolution": self.size[1],
                     "gl_z": -(numpy.sqrt(self.limit) / 4.)}
        # initial camera displacement (centres grid in viewport)
        init_z = -(numpy.sqrt(self.limit) / 4.)
        if init_z < -500:
            init_z = -500
        translate(self.view, -(self.init_pos / 2.)+.5,
            -(self.init_pos / 2.)+.5, -(numpy.sqrt(self.limit) / 4.))
        self.program['size'] = self.zoom['size']
        self.program['view'] = self.view
        self.program['model'] = self.model
        self.program['projection'] = self.projection

    def on_initialize(self, event):
        gloo.set_state(clear_color=self.bgcolour)

    def set_limit(self, lim):
        self.limit = lim

    def set_colour(self, colour, grid, coord):
        index = (self.init_pos**2) - (self.init_pos + self.init_pos*coord[1]) + coord[0]
        self.grid['colour'][index][0] = colour[0] / float(255)
        self.grid['colour'][index][1] = colour[1] / float(255)
        self.grid['colour'][index][2] = colour[2] / float(255)
        self.program['colour'] = gloo.VertexBuffer(self.grid['colour'].copy())

    def on_draw(self, event):
        gloo.clear()
        self.program.draw('points')

    def on_mouse_move(self, event):
        x, y = event.pos
        if not event.is_dragging:
            # point intersection
            to_gl = lambda c, i: (c / (.5 * float(self.size[i]))) - 1.
            mx = to_gl(x, 0)
            my = -to_gl(y, 1)
            #other = gluProject(0., 0., 0., self.view.astype('d'), self.projection.astype('d'), numpy.array([0., 0., self.size[0], self.size[1]]).astype('i'))
            return
        dx = +2 * ((x - event.last_event.pos[0]) / float(self.size[0]))
        dy = -2 * ((y - event.last_event.pos[1]) / float(self.size[1]))
        #                 v just a multiplier
        self.pan[0] -= dx * self.zoom['gl_z'] * 1.5
        self.pan[1] -= dy * self.zoom['gl_z'] * 1.5
        self.program['pan'] = self.pan
        self.update()

    def on_mouse_wheel(self, event):
        delta = event.delta[1]
        step = +.1 if delta > 0 else -.1
        zoom_ = zoom(self.zoom['size'], self.zoom['resolution'],
        self.zoom['gl_z'], step)
        translate(self.view, 0, 0, step)
        self.program['view'] = self.view
        self.zoom['size'] = zoom_
        self.zoom['gl_z'] += step
        self.program['size'] = self.zoom['size']
        self.update()
