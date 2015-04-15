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
    """Wrapper class for setting up a form as a Qt widget and tying it to a name.
    
    Extends QWidget.
    """
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.name = None
        self.form = None

    def set_form(self, name, form):
        self.name = name
        self.form = form
        self.form.setupUi(self)


class FormHandler():
    """Handles the forms for all of the different visualisations.
    
    The reasoning  was that since each  visualisation has differing settings, it
    seemed pertinent to dynamically load individual forms for each one.
    This class can set up forms, call a connection function from individual form
    handlers which sets up Slots/Signals for the form itself, retrieve data from
    these forms and remove the forms from the parent ui element.
    Each form itself has a corresponding module with a form.py file, which holds
    the boilerplate for the widget itself, and a handler.py which each contain a
    connection and retrieve function. These two functions  are both very similar
    throughout  all  different forms, and therefore the   functionality of these
    modules is implicit based on documentation in this class.

    Arguments:
        parent -- A Qt widget in which to place the form

    Attributes:
        form_handles -- A dictionary of handles to the form widgets themselves.
        form_wrapper -- The wrapper around whatever the  current form happens to
                        to be.
    """
    def __init__(self, parent):
        self.parent = parent
        self.form_handles = {"ulam": Ui_FormUlam(),
                             "sacks": Ui_FormSacks(),
                             "cloud": Ui_FormCloud(),
                             "complex": Ui_FormComplex(),
                             "simplegrid": Ui_FormSimpleGrid()}
        self.form_wrapper = None

    def setup_form(self, name):
        """Sets up a form to be displayed in the main ui and then shows it.
        
        Arguments:
            name -- the name of the  form to be  displayed (this  corresponds to
                    whatever name  is  used  for  the  form  in the form_handles
                    instance variable.
        """
        self.form_wrapper = FormWrapper()
        self.form_wrapper.set_form(name, self.form_handles[name])
        self.form_wrapper.setParent(self.parent)
        self.setup_connections(name)
        self.form_wrapper.show()

    def setup_connections(self, name):
        """Sets up Qt slogs/signals for a given form.

        This is useful for  enabling/disabling elements within  the form itself,
        and bears some correspondance  to the `set_specifics' function  found in
        some (or all) Generators.

        Arguments:
            name -- the name of the form to set up connections for.
        """
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
        """Retrieves data from the currently loaded form.

        This is done by calling the retrieve function found in the respective
        form handle module.

        Returns:
            All the data held in the current form.
        """
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
        """Removes the current form from the ui."""
        if self.form_wrapper:
            self.form_wrapper.setParent(None)
            del self.form_wrapper
            self.form_wrapper = None
