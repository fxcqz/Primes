from PyQt4 import QtGui, QtCore


def conn(form):
    QtCore.QObject.connect(form.dataset, \
        QtCore.SIGNAL("currentIndexChanged(QString)"), \
        lambda: form.gap.setEnabled(True) \
                if form.dataset.currentText() == "Prime Pairs" \
                else form.gap.setEnabled(False))


def retrieve(form):
    gap = int(form.gap.value())
    if str(form.dataset.currentText()) != "Prime Pairs":
        gap = None
    return {"dataset": str(form.dataset.currentText()),
            "min": int(form.min_.value()), "max": int(form.max_.value()),
            "gap": gap}
