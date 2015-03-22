from PyQt4 import QtGui, QtCore


def conn(form):
    QtCore.QObject.connect(form.dataset, \
        QtCore.SIGNAL("activated(QString)"), \
        lambda: form.gap.setEnabled(True) \
                if form.dataset.currentText() == "Prime Pairs" \
                else form.gap.setEnabled(False))


def retrieve(form):
    gap = int(form.gap.value())
    if str(form.dataset.currentText()) != "Prime Pairs":
        gap = None
    return str(form.dataset.currentText()), int(form.min_.value()), \
           int(form.max_.value()), gap
