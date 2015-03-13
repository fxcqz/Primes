import sys
from PyQt4 import QtGui, QtCore
from main_window import Ui_MainWindow


class StartGui(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

def run(argv):
    app = QtGui.QApplication(argv)
    myapp = StartGui()
    myapp.show()
    sys.exit(app.exec_())
