import sys
import numpy
from vispy import app, gloo
from vispy.util.transforms import perspective, translate, rotate, frustum


VERTEX = """
#version 120
attribute vec3 position;
attribute vec4 colour;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

uniform float size;

varying vec4 v_colour;

void main() {
    v_colour = colour;
    gl_Position = projection * model * view * vec4(position, 1.0);
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
    return ret

def zoom(size, resolution, gl_z, step):
    pix_z = gl_z * (resolution / 2.) # current
    new_z = (gl_z + step) * (resolution / 2.)
    ratio = pix_z / new_z
    return size * ratio

class Canvas(app.Canvas):
    def __init__(self, *args, **kwargs):
        app.Canvas.__init__(self, *args, **kwargs)
        self.program = gloo.Program(VERTEX, FRAGMENT)
        self.limit = 100 # of dataset
        grid = mg(self.limit, (1,1,1,1))
        grid['colour'][32][0] = 0
        # gl/gloo buffers
        verts = gloo.VertexBuffer(grid['position'].copy())
        self.program['position'] = verts
        self.program['colour'] = gloo.VertexBuffer(grid['colour'].copy())
        # view (camera) matrices
        self.view = numpy.eye(4, dtype=numpy.float32)
        self.model = numpy.eye(4, dtype=numpy.float32)
        self.projection = perspective(135., self.size[0] /
                                      float(self.size[1]), 0.1, 500.0)
        # initial camera position
        self.init_pos = int(numpy.ceil(self.limit ** 0.5))
        # zoom data
        #   size: sent to glsl to be gl_PointSize
        #   resolution: initial [comparative] grid size
        #   gl_z: size of z-value from camera to origin (in gl coords)
        self.zoom = {"size": self.size[1] / float(self.init_pos),
                     "resolution": self.size[1],
                     "gl_z": -(numpy.sqrt(self.limit) / 4.)}
        # initial camera displacement (centres grid in viewport)
        translate(self.view, -(self.init_pos / 2.)+.5,
            -(self.init_pos / 2.)+.5, -(numpy.sqrt(self.limit) / 4.))
        self.program['size'] = self.zoom['size']
        self.program['view'] = self.view
        self.program['model'] = self.model
        self.program['projection'] = self.projection

    def on_draw(self, event):
        gloo.clear()
        self.program.draw('points')

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


if __name__ == '__main__':
    c = Canvas(keys='interactive', size=(640.,480.))
    c.show()
    app.run()
