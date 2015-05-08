import sys
import os
import shutil
from PyQt4 import QtGui, QtCore
from threading import Thread
from tabbed_window import Ui_MainWindow

import primes.utils.handles as handles
from primes.utils.gl_pixdata import pixels_to_image
from form_handler import FormHandler


class StartGui(QtGui.QMainWindow):
    """This is  the  main GUI  class.  It  contains all  the functionality of ui
    elements, widgets and other  functionality required by the  program, such as
    saving visualisations as images.

    Attributes:
        ui -- Object automatically generated from a .ui file (using pyuic4).
              This object contains all of the widgets which are displayed in the
              ui.
        form_handler -- Dynamic form controller for loading  forms which display
                        settings unique to certain visualisations.
                        See the `form_handler' module for more information.
        gl_canvas -- Ui wide reference to  the object  which displays  an OpenGL
                     viewport.
        im_canvas -- A boolean which is True  or False depending on  whether the
                     ui is  currently displaying an  image. Unlike gl_canvas, an
                     image visualisation  is  taken from  a file  rather than an
                     object  so we  simply need to know whether there  is one or
                     not.

    Keyword Arguments:
        parent -- parent Qt widget (default None)
    """
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.form_handler = FormHandler(self.ui.specific_settings)
        self.setup_connections()
        self.form_handler.setup_form("ulam")
        self.gl_canvas = None
        self.im_canvas = False

    def setup_connections(self):
        """Sets up the Qt Signals and Slots for different Ui elements."""
        # layout form swapper
        QtCore.QObject.connect(self.ui.f_layout, \
            QtCore.SIGNAL("currentIndexChanged(QString)"), \
            lambda: self.form_swapper(self.ui.f_layout.currentText()))
        # graphics 
        QtCore.QObject.connect(self.ui.f_graphics, \
            QtCore.SIGNAL("currentIndexChanged(QString)"), \
            lambda: self.graphics_settings(self.ui.f_graphics.currentText()))
        # colour pickers
        QtCore.QObject.connect(self.ui.f_fg_button, \
            QtCore.SIGNAL("clicked()"), lambda: self.colour_picker("fg"))
        QtCore.QObject.connect(self.ui.f_bg_button, \
            QtCore.SIGNAL("clicked()"), lambda: self.colour_picker("bg"))
        # generate
        QtCore.QObject.connect(self.ui.generate, QtCore.SIGNAL("clicked()"), \
            self.generate)
        # menu items
        # new
        self.ui.actionNew.triggered.connect(self.new_visualisation)
        # save 
        self.ui.actionSave_As.triggered.connect(self.save)
        # exit
        self.ui.actionExit.triggered.connect(lambda: sys.exit())
        # about
        self.ui.actionAbout.triggered.connect(self.show_about)

    def check_tmp_storage(self):
        """Function which creates the temporary storage directory if it is not
        present.
        """
        if not os.path.exists("primes/tmp/"):
            os.makedirs("primes/tmp/")

    def visualise(self, vis):
        """Runs the generation of the visualisation and adds it to the Ui.

        Will generate  an image  or an  OpenGL visualisation  depending  on what 
        graphics choice has  been specified  by the  user. Conflicts between the
        visualisation and graphical basis are resolved by the ui itself.
        
        Arguments:
            vis -- visualisation object (see visualisation.generic)
        """
        QtGui.QApplication.processEvents()
        scn = QtGui.QGraphicsScene(self.ui.visualisation)
        self.ui.visualisation.setScene(scn)
        if vis != -1:
            self.remove_gl_canvas()
            if str(self.ui.f_graphics.currentText()) == 'Image (png)':
                gen_t = Thread(target=vis.to_image, args=("primes/tmp/v.png",))
                gen_t.start()
                gen_t.join()
                self.ui.main_tabs.setCurrentIndex(1)
                display = QtGui.QPixmap("primes/tmp/v.png")
                scn.addPixmap(display)
                self.im_canvas = True
            elif str(self.ui.f_graphics.currentText()) == 'OpenGL':
                # gl
                self.ui.main_tabs.setCurrentIndex(1)
                self.gl_canvas = vis.to_gl(self.ui.visualisation_tab)
                self.gl_canvas.show()
        else:
            scn.addText("Invalid Visualisation").setDefaultTextColor(QtGui.QColor(255, 255, 255))
        self.ui.generate.setEnabled(True)
        self.ui.generate.setText("Generate")
        self.ui.visualisation.show()

    def generate(self):
        """Collates information from the ui about the visualisation to be generated.

        This function will retrieve all the data specified by the  user, do some
        sanity  checks  on the data and then  instantiate a visualisation object
        based on  the layout name. It then calls  the  visualise  function which
        will generate the actual visualisation.
        """
        self.ui.generate.setText("Generating...")
        self.ui.generate.setEnabled(False)
        self.im_canvas = False
        # core settings
        form_data = self.form_handler.retrieve_data()
        layout = handles.visualisations[str(self.ui.f_layout.currentText())]
        dataset = handles.generators[form_data["dataset"]]
        width = int(self.ui.f_width.value())
        height = int(self.ui.f_height.value())
        min_ = form_data["min"]
        max_ = form_data["max"]
        bg_colour = QtGui.QColor(self.ui.f_bg_text.displayText())
        fg_colour = QtGui.QColor(self.ui.f_fg_text.displayText())
        visualisation = None
        if width > 0 and height > 0 and min_ <= max_:
            visualisation = layout(dataset.Generator,
                {"min": min_, "max": max_, 
                 "width": width, "height": height,
                 "colour": fg_colour.getRgb(),
                 "bgcolour": bg_colour.getRgb()})
            visualisation.generator.set_specifics(form_data)
            visualisation.set_specifics(form_data)
            if not visualisation.generator.runnable or not bg_colour.isValid() \
                    or not fg_colour.isValid():
                visualisation = -1
        else:
            visualisation = -1
        self.visualise(visualisation)

    def colour_picker(self, src):
        """Displays  a  colour  picker  for  choosing  background  or foreground
        colours which will be used in the visualisation.

        Arguments:
            src -- Source of the click which corresponds to either fg or bg.
        """
        picker = QtGui.QColorDialog(parent=self)
        colour = picker.getColor()
        if colour.isValid():
            if src == "fg":
                self.ui.f_fg_text.setText(str(colour.name()))
            elif src == "bg":
                self.ui.f_bg_text.setText(str(colour.name()))

    def remove_gl_canvas(self):
        """Removes the OpenGL canvas widget from the ui."""
        if self.gl_canvas is not None:
            self.gl_canvas.native.setVisible(False)
            self.gl_canvas.parent = None
            del self.gl_canvas
            self.gl_canvas = None

    def form_combinator(self):
        """Enables or disables certain ui elements depending on the combination
        of the graphics and layout QComboBoxes.

        This prevents jarring  error checking elsewhere  in the program. It made
        more sense to update the ui instead of presenting the user with numerous
        error messages.
        """
        graphics = str(self.ui.f_graphics.currentText())
        layout = str(self.ui.f_layout.currentText())
        if graphics == "Image (png)":
            if layout == "Simple Grid" or layout == "Wireframe":
                self.ui.generate.setEnabled(False)
            else:
                self.ui.generate.setEnabled(True)
        elif graphics == "OpenGL":
            if layout == "Data Cloud":
                self.ui.generate.setEnabled(False)
            else:
                self.ui.generate.setEnabled(True)

    def graphics_settings(self, name):
        """Enables or disables certain ui elements depending on the current
        value of the graphics QComboBox.

        Arguments:
            name -- The name of the graphics type currently selected.
        """
        self.form_combinator()
        if name == "OpenGL":
            self.ui.f_width.setEnabled(False)
            self.ui.f_height.setEnabled(False)
        elif name == "Image (png)":
            self.ui.f_width.setEnabled(True)
            self.ui.f_height.setEnabled(True)

    def form_swapper(self, name):
        """Function called by the signal from the user changing the layout."""
        self.form_combinator()
        self.form_handler.remove_form()
        if name == "Ulam Spiral":
            self.form_handler.setup_form("ulam")
        elif name == "Sacks Spiral":
            self.form_handler.setup_form("sacks")
        elif name == "Data Cloud":
            self.form_handler.setup_form("cloud")
        elif name == "Complex Plane":
            self.form_handler.setup_form("complex")
        elif name == "Simple Grid":
            self.form_handler.setup_form("simplegrid")
        elif name == "Wireframe":
            self.form_handler.setup_form("wireframe")

    def new_visualisation(self):
        """Reset values of the ui elements to what they are initially so the
        user can comfortably create a new visualisation.
        """
        self.ui.main_tabs.setCurrentIndex(0)
        self.ui.f_graphics.setCurrentIndex(0)
        self.ui.f_layout.setCurrentIndex(0)
        self.ui.f_width.setValue(250)
        self.ui.f_height.setValue(250)
        self.ui.f_fg_text.setText("#000000")
        self.ui.f_bg_text.setText("#FFFFFF")
        self.form_handler.remove_form()
        self.form_swapper(str(self.ui.f_layout.currentText()))
        self.remove_gl_canvas()

    def save(self):
        """Saves a visualisation as a png image.

        The function uses a QFileDialog to select a path to save the image in.
        """
        QtGui.QApplication.processEvents()
        if self.gl_canvas or self.im_canvas:
            filed = QtGui.QFileDialog(self)
            filename = str(filed.getSaveFileName(self, \
                "Save the Visualisation as an Image...", QtCore.QDir.homePath(), \
                ("Images (*.png)")))
            if filename:
                if filename.find(".png") == -1:
                    # append ".png" to the filename if it is missing
                    filename += ".png"
                if self.gl_canvas:
                    # save gl as img
                    pixels_to_image(self.gl_canvas.get_data(), (637, 437), "primes/tmp/v.png")
                if not os.path.exists(os.path.dirname(filename)):
                    os.makedirs(os.path.dirname(filename))
                if os.path.exists("primes/tmp/v.png"):
                    shutil.copy2("primes/tmp/v.png", filename)
                else:
                    err = QtGui.QMessageBox.warning(self, "An error occurred.", \
                        "No image data could be found, so your file was not saved.")

    def show_about(self):
        """Displays a message box with information about the program."""
        QtGui.QMessageBox.about(self, "About Prime Visualisation", \
            """Author:\tMatthew Rawcliffe\n"""
            """Year:\t2015\n"""
            """Info:\tMethods for visualising prime numbers\n"""
            """\tin 2 and 3 dimensional space.\n""")


def run(argv):
    """Runs the Ui and displays it.

    This function is called externally from the main file.
    """
    app = QtGui.QApplication(argv)
    main = StartGui()
    main.show()
    sys.exit(app.exec_())
