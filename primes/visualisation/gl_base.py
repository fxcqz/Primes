import sys
import numpy
from vispy import app, gloo
from vispy.util.transforms import perspective, translate
from OpenGL.GLU import gluUnProject


"""Provides a basic canvas and functions for instantiating, running and
displaying a visualisation on an OpenGL canvas using GL Points and Vispy.
"""

# Vertex Shader (glsl)
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

# Fragment Shader (glsl)
FRAGMENT = """
#version 120
varying vec4 v_colour;

void main() {
    gl_FragColor = v_colour;
}
"""

def mg(limit, colour=(1,0,0,1)):
    """`Make Grid' creates a 2d numpy array with two keys, Position and Colour.

    Position is an array of lists (of length 3) which hold x, y and z coords for
    each item  in the grid. The size of the  position array is based on a square
    grid determined by the size of the limit passed to  this function. The grids
    dimensions are calculated by square rooting the limit and rounding up (so no
    data  loss will  occur, and at  the worst there  will be some padding in the
    grid from additional space created by the rounding up.
    Colour is an  array of lists  (of length 4) which hold the r, g, b and alpha
    components of the colour of each element in the grid.
    The  indices of the  position and  colour arrays  match up  so that  for  an
    element `e' at index `i' in the position array, that elements colour will be
    found in the colour array at the same index `i'.

    Arguments:
        limit -- the upper limit of the dataset.

    Keyword Arguments:
        colour -- the default colour of all elemnts in the grid
                  (default (1,0,0,1)).

    Returns:
        A key  indexed numpy  dict of two 2d  numpy arrays,  position and colour
        which are used to represent a grid.
    """
    # dimension of the grid
    rows = int(numpy.ceil(limit ** 0.5))
    # the new limit based on the new dimensions
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
    """Zoom function used for zooming in and out of the Visualisation Canvas.

    Arguments:
        size -- Current size of the gl points.
        resolution -- modified resolution of the grid based on the initial size.
        gl_z -- the distance of the  camera from  the origin  plane (z-axis)  in
                gl coordinates.
        step -- the amount to zoom in (in gl coordinates).

    Returns:
        A new size to be used by the vertex shader for gl points  which has been
        multiplied by a zoom factor.
    """
    pix_z = gl_z * (resolution / 2.) # current
    new_z = (gl_z + step) * (resolution / 2.)
    ratio = pix_z / new_z
    return size * ratio

def norm_colour(colour):
    """Normalises a colour from it's 255 rgba values to values between 0 and 1.

    Arguments:
        colour -- a list representing an RGBA colour.

    Returns:
        A tuple of length 4 representing an  RGBA colour where  each element has
        been scaled from 0-255 to 0-1.
    """
    return (colour[0]/255., colour[1]/255., colour[2]/255., colour[3]/255.)

class Canvas(app.Canvas):
    """Basic OpenGL canvas using app.Canvas from Vispy.

    Uses the grid generated from `mg' and gl points to represent a visualisation
    similar to how colouring individual pixels would work in an image.

    Attributes:
        limit -- the upper limit of the dataset
        bgcolour -- background colour of the visualisation
        fgcolour -- foreground colour of the visualisation
        program -- handle to Program from vispy.gloo (this sends data to the
                   shaders).
        init_pos -- `initial position' used for initial calculations positioning
                    the grid.
        grid -- the grid generated by `mg'.
        view -- the view matrix used by opengl.
        model -- the model matrix used by opengl.
        projection -- the projection matrix used by opengl.
        pan -- the panning offset of the camera on the canvas.
        zoom -- dictionary of values pertaining to the calculation of the zoom.
                    * size: sent to glsl to be gl_PointSize
                    * resolution: initial [comparative] grid size
                    * gl_z: size of the z-value from camera to origin
                            (in gl coords).

    Keyword Arguments:
        limit -- the upper limit of the dataset
        bgcolour -- background colour of the visualisation
        fgcolour -- foreground colour of the visualisation
    For other args, see vispy.app.Canvas.
    """
    def __init__(self, *args, **kwargs):
        # override canvas constructor to obtain a limit
        self.limit = kwargs.pop('limit', None)
        self.bgcolour = norm_colour(kwargs.pop('bgcolour', None))
        self.fgcolour = norm_colour(kwargs.pop('fgcolour', None))
        app.Canvas.__init__(self, *args, **kwargs)
        app.use_app('PyQt4')
        self.program = gloo.Program(VERTEX, FRAGMENT)
        if self.limit is None:
            # default to 1000 if no limit is specified
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
        """Set a new limit for the visualisation"""
        self.limit = lim

    def set_colour(self, colour, grid, coord):
        """Sets an element in the grid to a given colour.

        This will  take  cartesian coords  as a tuple and  map them to the grid
        automatically.   This    is   where   (0, 0)  is  the  top   left   and 
        (sqrt(limit), sqrt(limit)) is the bottom right.

        Arguments:
            colour -- the colour to set the given point to (rgb or rgba).
            grid -- reference to the grid where the elements reside.
            coord -- tuple of the  location of the point in cartesian coords, of
                     the form (x, y).
        """
        index = (self.init_pos**2) - (self.init_pos + self.init_pos*coord[1]) + coord[0]
        self.grid['colour'][index][0] = colour[0] / float(255)
        self.grid['colour'][index][1] = colour[1] / float(255)
        self.grid['colour'][index][2] = colour[2] / float(255)
        self.program['colour'] = gloo.VertexBuffer(self.grid['colour'].copy())

    def on_draw(self, event):
        gloo.clear()
        self.program.draw('points')

    def on_mouse_move(self, event):
        """Handles mouse interaction with the canvas."""
        x, y = event.pos
        if not event.is_dragging:
            pixpan = (self.pan[0]*(1/self.size[0]), self.pan[1]*(1/self.size[1]))
            near = gluUnProject(x+pixpan[0], y+pixpan[1], 0., self.view.astype('d'), self.projection.astype('d'), numpy.array([0., 0., self.size[0], self.size[1]]).astype('i'))
            far = gluUnProject(x+pixpan[0], y+pixpan[1], 1., self.view.astype('d'), self.projection.astype('d'), numpy.array([0., 0., self.size[0], self.size[1]]).astype('i'))
            x_ = int(numpy.floor((((far[0] - near[0]) / float(500. - 0.5)) * near[2]) + near[0] + 0.5))
            y_ = int(numpy.floor(((((far[1] - near[1]) / float(500. - 0.5)) * near[2]) + near[1]) + 0.5))
            if x_ >= 0 and x_ < self.init_pos and y_ >= 0 and y_ < self.init_pos:
                self.set_colour((1,1,0), self.grid, (x_, y_))
                self.update()
            return
        dx = +2 * ((x - event.last_event.pos[0]) / float(self.size[0]))
        dy = -2 * ((y - event.last_event.pos[1]) / float(self.size[1]))
        #                 v just a multiplier
        self.pan[0] -= dx * self.zoom['gl_z'] * 1.5
        self.pan[1] -= dy * self.zoom['gl_z'] * 1.5
        self.program['pan'] = self.pan
        self.update()

    def on_mouse_wheel(self, event):
        """Handles mouse wheel events (just zoom in this case)."""
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

    def get_data(self):
        """Return the list of pixels currently displayed in the Canvas as a 3d
        numpy array.
        """
        return gloo.wrappers.read_pixels()
