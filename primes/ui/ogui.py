import sys
import os
from PyQt4 import QtGui, QtCore
from threading import Thread
from main_window import Ui_MainWindow

import primes.utils.handles as handles


class StartGui(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.make_connections()
        self.ui.progress_bar.hide()
        # VISUALISATION VARIABLES
        self.visualisation = None
        self.layout = handles.visualisations["Ulam Spiral"]
        self.dataset = handles.generators["Primes"]
        self.width = 0
        self.height = 0
        self.range_min = 0
        self.range_max = 0
        self.bgcolour = QtGui.QColor(0, 0, 0)
        self.fgcolour = QtGui.QColor(255, 255, 255)

    def make_connections(self):
        QtCore.QObject.connect(self.ui.img_bg_picker, QtCore.SIGNAL("clicked()"), lambda: self.colour_picker("bg"))
        QtCore.QObject.connect(self.ui.img_fg_picker, QtCore.SIGNAL("clicked()"), lambda: self.colour_picker("fg"))
        QtCore.QObject.connect(self.ui.generate, QtCore.SIGNAL("clicked()"), self.generate)

    def show_visualisation(self):
        QtGui.QApplication.processEvents()
        scn = QtGui.QGraphicsScene(self.ui.visualisation)
        self.ui.visualisation.setScene(scn)
        if self.visualisation != -1:
            gen_t = Thread(target=self.visualisation.to_image, args=("primes/tmp/v.png",))
            gen_t.start()
            gen_t.join()
            display = QtGui.QPixmap("primes/tmp/v.png")
            scn.addPixmap(display)
        else:
            scn.addText("Invalid Visualisation").setDefaultTextColor(QtGui.QColor(255, 255, 255))
        self.ui.visualisation.show()
        self.ui.generate.setEnabled(True)
        self.ui.generate.setText("Generate")

    def generate(self):
        self.ui.generate.setEnabled(False)
        self.ui.generate.setText("Generating...")
        # QCOMBO_BOX TEXT RETRIEVED VIA currentText
        self.layout = handles.visualisations[str(self.ui.img_layout_choice.currentText())]
        self.dataset = handles.generators[str(self.ui.img_dataset_choice.currentText())]
        self.width = int(self.ui.img_width_choice.value())
        self.height = int(self.ui.img_height_choice.value())
        self.range_min = int(self.ui.img_rmin_choice.value())
        self.range_max = int(self.ui.img_rmax_choice.value())
        self.bgcolour.setNamedColor(self.ui.img_bgcolour_choice.displayText())
        self.fgcolour.setNamedColor(self.ui.img_fgcolour_choice.displayText())
        if self.width > 0 and self.height > 0 and self.range_min <= self.range_max:
            self.visualisation = self.layout(self.dataset.Generator,
                                {"min": self.range_min,
                                 "max": self.range_max,
                                 "width": self.width,
                                 "height": self.height,
                                 "colour": self.fgcolour.getRgb(),
                                 "bgcolour": self.bgcolour.getRgb()})
            if not self.visualisation.generator.runnable:
                self.visualisation = -1
        else:
            self.visualisation = -1
        self.show_visualisation()

    def colour_picker(self, src):
        picker = QtGui.QColorDialog(parent=self)
        colour = picker.getColor()
        if src == "bg":
            if colour.isValid():
                self.ui.img_bgcolour_choice.setText(str(colour.name()))
                self.bgcolour = colour
        elif src == "fg":
            if colour.isValid():
                self.ui.img_fgcolour_choice.setText(str(colour.name()))
                self.fgcolour = colour

def run(argv):
    app = QtGui.QApplication(argv)
    main = StartGui()
    main.show()
    sys.exit(app.exec_())
