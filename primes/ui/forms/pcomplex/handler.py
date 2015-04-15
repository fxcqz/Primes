from PyQt4 import QtGui, QtCore
from primes.utils.custom_complex import CustomComplex


"""See FormHandler in primes.ui.form_handler for more info."""
def conn(form):
    pass


def retrieve(form):
    # some check for form of min/max input
    # prolly regex
    return {"dataset": str(form.dataset.currentText()),
            "min": CustomComplex(str(form.min_.displayText())),
            "max": CustomComplex(str(form.max_.displayText()))}
