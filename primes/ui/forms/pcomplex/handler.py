from PyQt4 import QtGui, QtCore


def conn(form):
    pass


def retrieve(form):
    # some check for form of min/max input
    # prolly regex
    return str(form.dataset.currentText()), int(form.min_.displayText()), \
           int(form.max_.displayText())
