from PyQt4 import QtGui, QtCore

from forms.ulam.form import Ui_FormUlam
from forms.sacks.form import Ui_FormSacks
from forms.cloud.form import Ui_FormCloud
from forms.pcomplex.form import Ui_FormComplex
from forms.simple_grid.form import Ui_FormSimpleGrid

import forms.ulam.handler as ulam_handler
import forms.sacks.handler as sacks_handler
import forms.cloud.handler as cloud_handler
import forms.pcomplex.handler as complex_handler
import forms.simple_grid.handler as sg_handler


class FormWrapper(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.name = None
        self.form = None

    def set_form(self, name, form):
        self.name = name
        self.form = form
        self.form.setupUi(self)


class FormHandler():
    def __init__(self, parent):
        self.parent = parent
        self.form_handles = {"ulam": Ui_FormUlam(),
                             "sacks": Ui_FormSacks(),
                             "cloud": Ui_FormCloud(),
                             "complex": Ui_FormComplex(),
                             "simplegrid": Ui_FormSimpleGrid()}
        self.form_wrapper = None

    def setup_form(self, name):
        self.form_wrapper = FormWrapper()
        self.form_wrapper.set_form(name, self.form_handles[name])
        self.form_wrapper.setParent(self.parent)
        self.setup_connections(name)
        self.form_wrapper.show()

    def setup_connections(self, name):
        if name == "ulam":
            ulam_handler.conn(self.form_wrapper.form)
        elif name == "sacks":
            sacks_handler.conn(self.form_wrapper.form)
        elif name == "cloud":
            cloud_handler.conn(self.form_wrapper.form)
        elif name == "complex":
            complex_handler.conn(self.form_wrapper.form)
        elif name == "simplegrid":
            sg_handler.conn(self.form_wrapper.form)

    def retrieve_data(self):
        ret = None
        if self.form_wrapper:
            form = self.form_wrapper.form
            if self.form_wrapper.name == "ulam":
                ret = ulam_handler.retrieve(form)
            elif self.form_wrapper.name == "sacks":
                ret = sacks_handler.retrieve(form)
            elif self.form_wrapper.name == "cloud":
                ret = cloud_handler.retrieve(form)
            elif self.form_wrapper.name == "complex":
                ret = complex_handler.retrieve(form)
            elif self.form_wrapper.name == "simplegrid":
                ret = sg_handler.retrieve(form)
        return ret

    def remove_form(self):
        if self.form_wrapper:
            self.form_wrapper.setParent(None)
            del self.form_wrapper
            self.form_wrapper = None
