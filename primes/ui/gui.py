import sys
from PyQt4 import QtGui, QtCore
from main_window import Ui_MainWindow

import primes.visualisation.ulam.ulam as ulam
import primes.generator.prime as prime


class StartGui(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.make_connections()
        # VISUALISATION VARIABLES
        self.visualisation = None
        self.layout = None
        self.dataset = None
        self.width = 0
        self.height = 0
        self.range_min = 0
        self.range_max = 1000
        self.bgcolour = QtGui.QColor(0, 0, 0)
        self.fgcolour = QtGui.QColor(255, 255, 255)

    def make_connections(self):
        QtCore.QObject.connect(self.ui.img_bg_picker, QtCore.SIGNAL("clicked()"), lambda: self.colour_picker("bg"))
        QtCore.QObject.connect(self.ui.img_fg_picker, QtCore.SIGNAL("clicked()"), lambda: self.colour_picker("fg"))
        QtCore.QObject.connect(self.ui.generate, QtCore.SIGNAL("clicked()"), self.generate)

    def generate(self):
        # QCOMBO_BOX TEXT RETRIEVED VIA currentText
        print self.ui.img_layout_choice.currentText()
        layout = None
        dataset = None
        self.width = int(self.ui.img_width_choice.value())
        self.height = int(self.ui.img_height_choice.value())
        self.range_min = int(self.ui.img_rmin_choice.value())
        self.range_max = int(self.ui.img_rmax_choice.value())
        # NEED SOME CHECK FOR COLOUR CHANGED FROM TEXT ONLY
        u = ulam.UlamSpiral(prime.Generator,
                            {"min": self.range_min,
                             "max": self.range_max,
                             "width": self.width,
                             "height": self.height,
                             "colour": self.fgcolour.getRgb(),
                             "bgcolour": self.bgcolour.getRgb()})
        #u.to_image("test.png")

    def colour_picker(self, src):
        picker = QtGui.QColorDialog(parent=self)
        colour = picker.getColor()
        if src == "bg":
            self.ui.img_bgcolour_choice.setText(str(colour.name()))
            self.bgcolour = colour
        elif src == "fg":
            self.ui.img_fgcolour_choice.setText(str(colour.name()))
            self.fgcolour = colour

def run(argv):
    app = QtGui.QApplication(argv)
    main = StartGui()
    main.show()
    sys.exit(app.exec_())