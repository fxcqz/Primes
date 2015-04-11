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

    def visualise(self, vis):
        QtGui.QApplication.processEvents()
        scn = QtGui.QGraphicsScene(self.ui.visualisation)
        self.ui.visualisation.setScene(scn)
        if vis != -1:
            if self.gl_canvas is not None:
                self.gl_canvas.native.setVisible(False)
                self.gl_canvas.parent = None
                del self.gl_canvas
                self.gl_canvas = None
            if str(self.ui.f_graphics.currentText()) == 'Image (png)':
                gen_t = Thread(target=vis.to_image, args=("primes/tmp/v.png",))
                gen_t.start()
                gen_t.join()
                self.ui.main_tabs.setCurrentIndex(1)
                #maybe error check this filepath
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
        # error check these colours
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
        picker = QtGui.QColorDialog(parent=self)
        colour = picker.getColor()
        if colour.isValid():
            if src == "fg":
                self.ui.f_fg_text.setText(str(colour.name()))
            elif src == "bg":
                self.ui.f_bg_text.setText(str(colour.name()))

    def form_combinator(self):
        graphics = str(self.ui.f_graphics.currentText())
        layout = str(self.ui.f_layout.currentText())
        if graphics == "Image (png)":
            if layout == "Simple Grid":
                self.ui.generate.setEnabled(False)
            else:
                self.ui.generate.setEnabled(True)
        elif graphics == "OpenGL":
            if layout == "Data Cloud":
                self.ui.generate.setEnabled(False)
            else:
                self.ui.generate.setEnabled(True)

    def graphics_settings(self, name):
        self.form_combinator()
        if name == "OpenGL":
            self.ui.f_width.setEnabled(False)
            self.ui.f_height.setEnabled(False)
        elif name == "Image (png)":
            self.ui.f_width.setEnabled(True)
            self.ui.f_height.setEnabled(True)

    def form_swapper(self, name):
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

    def new_visualisation(self):
        self.ui.main_tabs.setCurrentIndex(0)
        self.ui.f_graphics.setCurrentIndex(0)
        self.ui.f_layout.setCurrentIndex(0)
        self.ui.f_width.setValue(250)
        self.ui.f_height.setValue(250)
        self.ui.f_fg_text.setText("#000000")
        self.ui.f_bg_text.setText("#FFFFFF")
        self.form_handler.remove_form()
        self.form_swapper(str(self.ui.f_layout.currentText()))

    def save(self):
        QtGui.QApplication.processEvents()
        if self.gl_canvas or self.im_canvas:
            filed = QtGui.QFileDialog(self)
            filename = str(filed.getSaveFileName(self, \
                "Save the Visualisation as an Image...", QtCore.QDir.homePath(), \
                ("Images (*.png)")))
            if not filename.find(".png"):
                filename += ".png"
            if self.gl_canvas:
                # save gl as img
                pixels_to_image(self.gl_canvas.get_data(), (637, 437), "primes/tmp/v.png")
            if os.path.exists("primes/tmp/v.png"):
                shutil.copy2("primes/tmp/v.png", filename)
            else:
                err = QtGui.QMessageBox.warning(self, "An error occurred.", \
                    "No image data could be found, so your file was not saved.")

    def show_about(self):
        QtGui.QMessageBox.about(self, "About Prime Visualisation", \
            """Author:\tMatthew Rawcliffe\n"""
            """Year:\t2015\n"""
            """Info:\tMethods for visualising prime numbers\n"""
            """\tin 2 and 3 dimensional space.\n""")


def run(argv):
    app = QtGui.QApplication(argv)
    main = StartGui()
    main.show()
    sys.exit(app.exec_())
