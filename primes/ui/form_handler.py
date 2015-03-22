from PyQt4 import QtGui, QtCore

from forms.form_ulam import Ui_FormUlam


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
        print self.retrieve_data()

    def setup_connections(self, name):
        if name == "ulam":
            QtCore.QObject.connect(self.form_wrapper.form.dataset, \
                QtCore.SIGNAL("activated(QString)"), \
                lambda: self.form_wrapper.form.gap.setEnabled(True) \
                        if self.form_wrapper.form.dataset.currentText() == "Prime Pairs" \
                        else self.form_wrapper.form.gap.setEnabled(False))

    def retrieve_data(self):
        if self.form_wrapper:
            form = self.form_wrapper.form
            if self.form_wrapper.name == "ulam":
                gap = int(form.gap.value())
                if str(form.dataset.currentText()) != "Prime Pairs":
                    gap = None
                return str(form.dataset.currentText()), int(form.min_.value()), int(form.max_.value()), gap

    def remove_form(self):
        self.form_wrapper.setParent(None)
        del self.form_wrapper
        self.form_wrapper = None
