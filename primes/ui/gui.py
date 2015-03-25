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
        QtCore.QObject.connect(self.ui.f_layout, \
            QtCore.SIGNAL("currentIndexChanged(QString)"), \
            lambda: self.form_swapper(self.ui.f_layout.currentText()))

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
