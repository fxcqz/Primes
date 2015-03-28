import sys
import os
from PyQt4 import QtGui, QtCore
from threading import Thread
from tabbed_window import Ui_MainWindow

import primes.utils.handles as handles
from form_handler import FormHandler


class StartGui(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.form_handler = FormHandler(self.ui.specific_settings)
        self.setup_connections()
        self.form_handler.setup_form("ulam")

    def setup_connections(self):
        # layout form swapper
        QtCore.QObject.connect(self.ui.f_layout, \
            QtCore.SIGNAL("currentIndexChanged(QString)"), \
            lambda: self.form_swapper(self.ui.f_layout.currentText()))
        # colour pickers
        QtCore.QObject.connect(self.ui.f_fg_button, \
            QtCore.SIGNAL("clicked()"), lambda: self.colour_picker("fg"))
        QtCore.QObject.connect(self.ui.f_bg_button, \
            QtCore.SIGNAL("clicked()"), lambda: self.colour_picker("bg"))
        # generate
        QtCore.QObject.connect(self.ui.generate, QtCore.SIGNAL("clicked()"), \
            self.generate)

    def visualise(self, vis):
        QtGui.QApplication.processEvents()
        scn = QtGui.QGraphicsScene(self.ui.visualisation)
        self.ui.visualisation.setScene(scn)
        if vis != -1:
            gen_t = Thread(target=vis.to_image, args=("primes/tmp/v.png",))
            gen_t.start()
            gen_t.join()
            # maybe error check this filepath
            display = QtGui.QPixmap("primes/tmp/v.png")
            scn.addPixmap(display)
        else:
            scn.addText("Invalid Visualisation").setDefaultTextColor(QtGui.QColor(255, 255, 255))
        self.ui.generate.setEnabled(True)
        self.ui.generate.setText("Generate")
        self.ui.main_tabs.setCurrentIndex(1)
        self.ui.visualisation.show()

    def generate(self):
        self.ui.generate.setEnabled(False)
        self.ui.generate.setText("Generating...")
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
            if not visualisation.generator.runnable:
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

    def form_swapper(self, name):
        self.form_handler.remove_form()
        if name == "Ulam Spiral":
            self.form_handler.setup_form("ulam")
        elif name == "Sacks Spiral":
            self.form_handler.setup_form("sacks")
        elif name == "Data Cloud":
            self.form_handler.setup_form("cloud")
        elif name == "Complex Plane":
            self.form_handler.setup_form("complex")


def run(argv):
    app = QtGui.QApplication(argv)
    main = StartGui()
    main.show()
    sys.exit(app.exec_())
