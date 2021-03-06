import sys
import numpy
from vispy import app, gloo
from vispy.util.transforms import perspective, translate
from OpenGL.GLU import gluUnProject
import primes.utils.poly as poly


"""Provides a basic canvas and functions for instantiating, running and
displaying a visualisation on an OpenGL canvas using GL Points and Vispy.
"""

# Vertex Shader (glsl)
VERTEX = """
#version 120
attribute vec3 position;
attribute vec4 colour;

/* `booleans' */
attribute float toggled;
attribute float highlighted;

/* matrices */
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

/* camera stuff */
uniform float size;
uniform vec2 pan;

/* highlight and toggle colours */
uniform vec4 t_colour;
uniform vec4 h_colour;

varying vec4 v_colour;

varying float v_toggled;
varying float v_highlighted;

void main() {
    v_colour = colour;
    
    v_toggled = toggled;
    v_highlighted = highlighted;

    gl_Position = projection * model * view * vec4(position + vec3(pan[0], pan[1], 0.0), 1.0);
    gl_PointSize = size;
}
"""

# Fragment Shader (glsl)
FRAGMENT = """
#version 120
uniform vec4 t_colour;
uniform vec4 h_colour;

varying float v_toggled;
varying float v_highlighted;

varying vec4 v_colour;

void main() {
    gl_FragColor = v_colour;
    if(v_highlighted > 0.5){
        gl_FragColor = h_colour;
    } else if(v_toggled > 0.5){
        gl_FragColor = t_colour;
    }
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
    ret = numpy.zeros(n, dtype=[("position", 'f4', 3), ("colour", 'f4', 4),
                                ("toggled", 'f4', 1), ("highlighted", 'f4', 1)])
    ret["position"] = numpy.array(points)
    ret["colour"] = colour
    ret["toggled"] = 0.0
    ret["highlighted"] = 0.0
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
    return (colour[0]/255., colour[1]/255., colour[2]/255., 1.)

class Canvas(app.Canvas):
    """Basic OpenGL canvas using app.Canvas from Vispy.

    Uses the grid generated from `mg' and gl points to represent a visualisation
    similar to how colouring individual pixels would work in an image.

    Attributes:
        limit -- the upper limit of the dataset
        bgcolour -- background colour of the visualisation
        fgcolour -- foreground colour of the visualisation
        data -- the dataset which is being visualised
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
        self.data = kwargs.pop('data', None)
        app.Canvas.__init__(self, *args, **kwargs)
        app.use_app('PyQt4')
        self.program = gloo.Program(VERTEX, FRAGMENT)
        # default vals for essential variables if absent in kwargs
        if self.limit is None:
            # default to 1000 if no limit is specified
            self.limit = 1000
        if self.bgcolour is None or self.fgcolour is None:
            self.bgcolour = (1,1,1,1)
            self.fgcolour = (0,0,0,1)
        self.init_pos = int(numpy.ceil(self.limit ** 0.5))
        self.grid = mg(self.limit, self.bgcolour)
        # gl/gloo buffers
        verts = gloo.VertexBuffer(self.grid['position'].copy())
        self.program['position'] = verts
        self.program['colour'] = gloo.VertexBuffer(self.grid['colour'].copy())
        self.program['toggled'] = gloo.VertexBuffer(self.grid['toggled'].copy())
        self.program['highlighted'] = gloo.VertexBuffer(self.grid['highlighted'].copy())
        self.toggle_data = {}
        # calc selection colours & send to buf
        sel_colours = self.get_selection_colours()
        self.program['t_colour'] = sel_colours["toggled"]
        self.program['h_colour'] = sel_colours["highlighted"]
        # view (camera) matrices
        self.view = numpy.eye(4, dtype=numpy.float32)
        self.model = numpy.eye(4, dtype=numpy.float32)
        self.program['model'] = self.model
        # initial camera displacement (centres grid in viewport)
        init_z = -(numpy.sqrt(self.limit) / 4.)
        if init_z < -500:
            init_z = -500
        translate(self.view, -(self.init_pos / 2.) + 0.5,
                  -(self.init_pos / 2.) + 0.5, init_z)
        self.program['view'] = self.view
        # the purpose of setting the near limit to 0.5 is that at any distance
        # nearer the points, the zooming stops working
        self.projection = perspective(135., self.size[0] /
                                      float(self.size[1]), 0.5, 500.)
        self.program['projection'] = self.projection
        # initial camera position
        self.pan = self.program['pan'] = [0., 0.]
        # zoom data
        #   size: sent to glsl to be gl_PointSize
        #   resolution: initial [comparative] grid size
        #   gl_z: size of z-value from camera to origin (in gl coords)
        self.zoom = {"size": self.size[1] / float(self.init_pos),
                     "resolution": self.size[1],
                     "gl_z": -(numpy.sqrt(self.limit) / 4.)}
        self.program['size'] = self.zoom['size']

    def on_initialize(self, event):
        """Init event. Colours all points found in the dataset."""
        gloo.set_state(clear_color=self.bgcolour)
        # colour all data elements
        if self.data is not None:
            try:
                for elem in self.data:
                    self.set_colour(self.fgcolour, self.grid, (elem[0], elem[1]))
            except IndexError:
                pass

    def get_selection_colours(self):
        """Initialise the colours used for highlighting and toggling cells."""
        t_colour = ((self.bgcolour[0]+self.fgcolour[0])/2.,
                    (self.bgcolour[1]+self.fgcolour[1])/2.,
                    (self.bgcolour[2]+self.fgcolour[2])/2.,
                    1.)
        h_colour = ((t_colour[0]+self.fgcolour[0])/2.,
                    (t_colour[1]+self.fgcolour[1])/2.,
                    (t_colour[2]+self.fgcolour[2])/2.,
                    1.)
        return {"toggled": t_colour, "highlighted": h_colour}

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
        self.grid['colour'][index][0] = colour[0]
        self.grid['colour'][index][1] = colour[1]
        self.grid['colour'][index][2] = colour[2]
        self.program['colour'] = self.grid['colour'].copy()

    def on_draw(self, event):
        """Draw event."""
        gloo.clear()
        self.program.draw('points')

    def coord_to_index(self, x, y):
        """Converts a coordinate to an index in the grid array"""
        return (self.init_pos**2) - (self.init_pos + self.init_pos*y) + x

    def mouse_gl_pos(self, x, y):
        """Gets the location of the cursor in world coordinates.
        
        Arguments:
            x -- x position of the cursor in pixels
            y -- y position of the cursor in pixels
        """
        # use a recontruction of the viewport since we have no baseline
        # handle with vispy (6th param of gluUnProject)
        near = gluUnProject(x, y, 0.,
            self.view.astype('d'),
            self.projection.astype('d'),
            numpy.array([0., 0., self.size[0], self.size[1]]).astype('i'))
        far = gluUnProject(x, y, 1.,
            self.view.astype('d'),
            self.projection.astype('d'),
            numpy.array([0., 0., self.size[0], self.size[1]]).astype('i'))
        # x and y position of cursor in world coordinates
        x_ = int(numpy.floor((((far[0] - near[0]) / float(500. - 0.5)) * near[2]) + near[0] + 0.5 - self.pan[0]))
        y_ = int(numpy.floor(((((far[1] - near[1]) / float(500. - 0.5)) * near[2]) + near[1]) + 0.5 + self.pan[1]))
        return x_, y_

    def find_in_data(self, x, y):
        """Finds the element of an array for a given x and y coordinate."""
        for elem in self.data:
            if elem[0] == x and elem[1] == y:
                return elem
        return None

    def colour_polynomial(self, polynomial):
        """Colours all values found in a given polynomial."""
        for p in polynomial:
            for elem in self.data:
                if p == elem[2]:
                    self.grid['toggled'][self.coord_to_index(elem[0], elem[1])] = 1.0
                    self.toggle_data[self.coord_to_index(elem[0], elem[1])] = elem[2]
                    break

    def on_mouse_release(self, event):
        """Handles the selection of points and fitting polynomials to them."""
        # only interested about right clicks (since left click drags)
        if self.data is not None:
            if isinstance(self.data[0], complex):
                # polynomial fitting doesnt work for complex numbers
                return
        if event.button == 2:
            x, y = self.mouse_gl_pos(event.pos[0], event.pos[1])
            if x >= 0 and x < self.init_pos and y >= 0 and y < self.init_pos:
                index = self.coord_to_index(x, y)
                if self.grid['toggled'][index] > 0.5:
                    # if already toggled, untoggle
                    self.grid['toggled'][index] = 0.0
                    del self.toggle_data[index]
                else:
                    # if untoggled, toggle
                    self.grid['toggled'][index] = 1.0
                    self.toggle_data[index] = self.find_in_data(x, y)
                if len(self.toggle_data) >= 4:
                    # reset all toggled points
                    self.grid['toggled'] = 0.0
                    self.toggle_data = {}
                try:
                    if len(self.toggle_data) == 3:
                        # polynomial interpolation
                        roots = [e[2] for e in self.toggle_data.values()]
                        polynomial = poly.poly_vals_in_range(1, self.limit, roots)
                        self.colour_polynomial(polynomial)
                except TypeError:
                    pass
                self.program['toggled'] = self.grid['toggled'].copy()
            self.update()

    def on_mouse_move(self, event):
        """Handles mouse interaction with the canvas."""
        x, y = event.pos
        if not event.is_dragging:
            mouse_pos = self.mouse_gl_pos(x, y)
            x_ = mouse_pos[0]
            y_ = mouse_pos[1]
            # determine whether the cursor is colliding with a point in the grid
            # shift all lines below until return into if statement if it causes
            # speed/framerate issues
            self.grid["highlighted"] = 0.0
            if x_ >= 0 and x_ < self.init_pos and y_ >= 0 and y_ < self.init_pos:
                # set the highlighted grid point to be toggled
                self.grid["highlighted"][self.coord_to_index(x_, y_)] = 1.0
            self.program['highlighted'] = self.grid['highlighted'].copy()
            self.update()
            return
        if event.button == 1:
            dx = +2 * ((x - event.last_event.pos[0]) / float(self.size[0]))
            dy = -2 * ((y - event.last_event.pos[1]) / float(self.size[1]))
            #                 v just a multiplier
            self.pan[0] -= dx * self.zoom['gl_z'] * 2.0
            self.pan[1] -= dy * self.zoom['gl_z'] * 2.0
            self.program['pan'] = self.pan
            self.update()

    def on_mouse_wheel(self, event):
        """Handles mouse wheel events (just zoom in this case)."""
        delta = event.delta[1]
        # uses step proportionate to zoom level (so zooming doesnt take forever)
        inner_step = abs(self.zoom['gl_z'] / 10.)
        step = inner_step if delta > 0 else -inner_step
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
