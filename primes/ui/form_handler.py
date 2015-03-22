from PyQt4 import QtGui, QtCore

from forms.ulam.form import Ui_FormUlam
import forms.ulam.handler as ulam_handler


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
        self.form_handles = {"ulam": Ui_FormUlam()}
        self.form_wrapper = None

    def setup_form(self, name):
        form = FormWrapper()
        form.set_form(name, self.form_handles[name])
        form.setParent(self.parent)
        self.form_wrapper = form
        self.setup_connections(name)

    def setup_connections(self, name):
        if name == "ulam":
            ulam_handler.conn(self.form_wrapper.form)

    def retrieve_data(self):
        ret = None
        if self.form_wrapper:
            form = self.form_wrapper.form
            if self.form_wrapper.name == "ulam":
                ret = ulam_handler.retrieve(form)
        return ret

    def remove_form(self):
        self.form_wrapper.setParent(None)
        del self.form_wrapper
        self.form_wrapper = None
