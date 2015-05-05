import numpy
from vispy import gloo, app
from vispy.util.transforms import perspective, translate, xrotate, yrotate, zrotate


VERTEX = """
#version 120
attribute vec3 position;
attribute vec4 colour;

uniform mat4 view;
uniform mat4 model;
uniform mat4 projection;

varying vec4 v_colour;

void main(){
    v_colour = colour;
    gl_Position = projection * view * model * vec4(position, 1.0);
}
"""
FRAGMENT = """
#version 120
varying vec4 v_colour;

void main(){
    gl_FragColor = v_colour;
}
"""

class Canvas(app.Canvas):
    def __init__(self, *args, **kwargs):
        # visualisation args
        self.limit = kwargs.pop('limit', None)
        self.data = kwargs.pop('data', None)
        self.bgcolour = kwargs.pop('bgcolour', None)
        self.fgcolour = kwargs.pop('fgcolour', None)
        self.colour_check()
        # ##################
        app.Canvas.__init__(self, *args, **kwargs)
        self.program = gloo.Program(VERTEX, FRAGMENT)
        self.dimension = int(numpy.ceil(self.limit ** 0.5))
        self.grid = self.make_grid()
        self.program['position'] = self.grid['position']
        self.program['colour'] = self.grid['colour']
        self.projection = perspective(90., self.size[0] /
                                      float(self.size[1]), 0.5, 500.)
        self.program['projection'] = self.projection
        self.view = numpy.eye(4, dtype=numpy.float32)
        self.camerapos = [-1,0,-5]
        self.zoom = self.camerapos[2]
        translate(self.view, self.camerapos[0], self.camerapos[1], self.camerapos[2])
        self.program['view'] = self.view
        self.model = numpy.eye(4, dtype=numpy.float32)
        self.model_vars = {"r": {'x': -45, 'y': 0}, "t": [1.5, 0, 1.5]}
        xrotate(self.model, self.model_vars['r']['x'])
        yrotate(self.model, self.model_vars['r']['y'])
        translate(self.model, self.model_vars['t'][0], self.model_vars['t'][1],
                  self.model_vars['t'][2])
        self.program['model'] = self.model

    def on_initialize(self, event):
        gloo.set_state(clear_color=self.bgcolour)

    def on_draw(self, event):
        gloo.clear()
        self.program.draw('lines')

    def on_key_press(self, event):
        k = event.key
        self.model = numpy.eye(4, dtype=numpy.float32)
        if k == 'Left':
            self.model_vars['r']['y'] -= 5
        elif k == 'Right':
            self.model_vars['r']['y'] += 5
        if k == 'Up':
            self.model_vars['r']['x'] -= 5
        elif k == 'Down':
            self.model_vars['r']['x'] += 5
        xrotate(self.model, self.model_vars['r']['x'])
        yrotate(self.model, self.model_vars['r']['y'])
        translate(self.model, self.model_vars['t'][0], self.model_vars['t'][1],
                  self.model_vars['t'][2])
        self.program['model'] = self.model
        self.update()

    def on_mouse_wheel(self, event):
        delta = event.delta[1]
        step = 1 if delta > 0 else -1
        self.zoom += step
        translate(self.view, 0, 0, step)
        self.program['view'] = self.view
        self.update()

    def on_mouse_move(self, event):
        if not event.is_dragging:
            return
        x, y = event.pos
        dx = +2 * ((x - event.last_event.pos[0]) / float(self.size[0]))
        dy = -2 * ((y - event.last_event.pos[1]) / float(self.size[1]))
        #                 v just a multiplier
        translate(self.view, 0.75 * dx * abs(self.zoom), 0.75 * dy * abs(self.zoom), 0)
        self.program['view'] = self.view
        self.update()

    def make_grid(self):
        n = self.dimension ** 2
        points = []
        # initialise all points in the grid
        for z in range(self.dimension):
            for x in range(self.dimension):
                y = 0.5 if ((self.dimension*z) + x + 1) in self.data else 0
                points.append([x-(self.dimension/2.), y, z-(self.dimension/2.)])
        positions = []
        # order the points like for vertices so grid draws correctly
        for x in range(self.dimension):
            # horize
            mult = x * self.dimension
            for p in range(self.dimension-1):
                positions.append(points[mult+p])
                positions.append(points[mult+p+1])
        for z in range(n-self.dimension):
            # vert
            positions.append(points[z])
            positions.append(points[z+self.dimension])
        grid = numpy.zeros(4*(self.dimension-1)*self.dimension,
                           dtype=[("position", 'f4', 3), ("colour", 'f4', 4)])
        grid['position'] = numpy.array(positions)
        grid['colour'] = self.fgcolour
        return grid

    def colour_check(self):
        if self.bgcolour is None:
            self.bgcolour = (1,1,1,1)
        else:
            self.bgcolour = (self.bgcolour[0]/255.,
                             self.bgcolour[1]/255.,
                             self.bgcolour[2]/255.,
                             self.bgcolour[3]/255.)
        if self.fgcolour is None:
            self.fgcolour = (0,0,0,1)
        else:
            self.fgcolour = (self.fgcolour[0]/255.,
                             self.fgcolour[1]/255.,
                             self.fgcolour[2]/255.,
                             self.fgcolour[3]/255.)
