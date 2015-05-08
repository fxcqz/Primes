from PyQt4 import QtGui, QtCore


"""See FormHandler in primes.ui.form_handler for more info."""
def conn(form):
    QtCore.QObject.connect(form.dataset, \
        QtCore.SIGNAL("currentIndexChanged(QString)"), \
        lambda: form.gap.setEnabled(True) \
                if form.dataset.currentText() == "Prime Pairs" \
                else form.gap.setEnabled(False))
    QtCore.QObject.connect(form.dataset, \
        QtCore.SIGNAL("currentIndexChanged(QString)"), \
        lambda: form.big_data.setEnabled(True) \
                if form.dataset.currentText() == "Big Dataset" \
                else form.big_data.setEnabled(False))


def retrieve(form):
    gap = int(form.gap.value())
    if str(form.dataset.currentText()) != "Prime Pairs":
        gap = None
    return {"dataset": str(form.dataset.currentText()),
            "min": int(form.min_.value()), "max": int(form.max_.value()),
            "gap": gap, "mod": int(form.mod_.value()),
            "big": str(form.big_data.currentText())}
