from PyQt4 import QtGui, QtCore


def conn(form):
    pass


def retrieve(form):
    # some check for form of min/max input
    # prolly regex
    return {"dataset": str(form.dataset.currentText()), \
            "min": int(form.min_.displayText()), \
            "max": int(form.max_.displayText())}
