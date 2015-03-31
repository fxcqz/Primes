import math
import numpy as np

from vispy import gloo
from vispy import app


# limit
lim = 10000
# rows
n_ = int(math.ceil(lim ** 0.5))
# total number of points
n = n_ ** 2
# point size
psz = 3
pts = []
#offsets
xoff = -1.0 + 2 * ((0.5 * (640.0 - (n_ * psz))) / 640.0)
yoff = 1.0 - 2 * ((0.5 * (480.0 - (n_ * psz))) / 480.0)
for y in range(n_):
    pts.append([])
    for x in range(n_):
        pts[y].append([])
        pts[y][-1].append(xoff + (x*(2*psz/640.0)))
        pts[y][-1].append(yoff - (y*(2*psz/480.0)))
        pts[y][-1].append(0.0)
pts = np.array(pts).reshape(n,3)

points = np.zeros(n, dtype=[('position', 'f4', 3),
                      ('colour', 'f4', 4),
                      ('size', 'f4', 1)])
points['size'] = psz
points['colour'] = 0,1,0,1
points['position'] = pts
points['colour'][0][1] = 0.0
points['colour'][1][0] = 1.0
points['colour'][1][1] = 0.0

VERT_SHADER = """
#version 120
attribute vec3 position;
attribute vec4 colour;
attribute float size;

varying vec4 v_color;
void main(void){
    gl_Position = vec4(position, 1.0);
    v_color = colour;
    gl_PointSize = size;
}
"""

FRAG_SHADER = """
#version 120
varying vec4 v_color;
void main() {
    float x = 1.0 * gl_PointCoord.x - 1.0;
    float y = 1.0 * gl_PointCoord.y - 1.0;
    float a = 1.0 - (x*x + y*y);
    gl_FragColor = vec4(v_color.rgb, a * v_color.a);
}
"""

class Canvas(app.Canvas):
    def __init__(self):
        app.Canvas.__init__(self, keys='interactive')
        self.program = gloo.Program(VERT_SHADER, FRAG_SHADER)
        self.size = (640, 480)
        # bufs
        self.vbo_position = gloo.VertexBuffer(points['position'].copy())
        self.vbo_colour = gloo.VertexBuffer(points['colour'].copy())
        self.vbo_size = gloo.VertexBuffer(points['size'].copy())
        # bind
        self.program['colour'] = self.vbo_colour
        self.program['size'] = self.vbo_size
        self.program['position'] = self.vbo_position

    def on_initialize(self, event):
        gloo.set_state(clear_color=(1, 1, 1, 1), blend=False)

    #def on_resize(self, event):
    #    width, height = event.size
    #    gloo.set_viewport(0, 0, width, height)

    def on_draw(self, event):
        gloo.clear()
        self.program.draw('points')

    def on_mouse_release(self, event):
        print event.pos


if __name__ == '__main__':
    c = Canvas()
    c.show()
    app.run()
