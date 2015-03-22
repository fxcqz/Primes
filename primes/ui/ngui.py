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
        self.form_handler.setup_form("ulam")
        #self.form_handler.remove_form()


def run(argv):
    app = QtGui.QApplication(argv)
    main = StartGui()
    main.show()
    sys.exit(app.exec_())
