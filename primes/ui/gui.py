import sys
from PyQt4 import QtGui, QtCore
from main_window import Ui_MainWindow


class StartGui(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.make_connections()
        # VISUALISATION VARIABLES
        self.layout = None
        self.dataset = None
        self.width = None
        self.height = None
        self.range_min = None
        self.range_max = None
        self.bgcolour = None
        self.fgcolour = None

    def make_connections(self):
        QtCore.QObject.connect(self.ui.img_bg_picker, QtCore.SIGNAL("clicked()"), lambda: self.colour_picker("bg"))
        QtCore.QObject.connect(self.ui.img_fg_picker, QtCore.SIGNAL("clicked()"), lambda: self.colour_picker("fg"))
        QtCore.QObject.connect(self.ui.img_width_choice, QtCore.SIGNAL("valueChanged()"), lambda: self.update_from_spin("width"))
        QtCore.QObject.connect(self.ui.generate, QtCore.SIGNAL("clicked()"), self.generate)

    def update_from_spin(self, arg):
        print "called"
        if arg == "width":
            self.width = int(self.ui.img_width_choice.value())

    def generate(self):
        layout = None
        dataset = None
        width = None
        height = None
        range_min = None
        range_max = None
        print self.width

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
