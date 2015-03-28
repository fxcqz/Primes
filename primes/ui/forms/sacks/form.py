# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sacks.ui'
#
# Created: Sat Mar 28 00:18:47 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_FormSacks(object):
    def setupUi(self, FormSacks):
        FormSacks.setObjectName(_fromUtf8("FormSacks"))
        FormSacks.resize(391, 411)
        self.groupBox = QtGui.QGroupBox(FormSacks)
        self.groupBox.setGeometry(QtCore.QRect(10, 20, 371, 111))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.max_ = QtGui.QSpinBox(self.groupBox)
        self.max_.setGeometry(QtCore.QRect(80, 72, 101, 20))
        self.max_.setMaximum(999999999)
        self.max_.setProperty("value", 62750)
        self.max_.setObjectName(_fromUtf8("max_"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(20, 22, 50, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(16, 46, 54, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.min_ = QtGui.QSpinBox(self.groupBox)
        self.min_.setGeometry(QtCore.QRect(80, 46, 101, 20))
        self.min_.setMaximum(999999999)
        self.min_.setObjectName(_fromUtf8("min_"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(13, 72, 57, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.dataset = QtGui.QComboBox(self.groupBox)
        self.dataset.setGeometry(QtCore.QRect(80, 20, 101, 20))
        self.dataset.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.dataset.setObjectName(_fromUtf8("dataset"))
        self.dataset.addItem(_fromUtf8(""))
        self.dataset.addItem(_fromUtf8(""))
        self.groupBox_2 = QtGui.QGroupBox(FormSacks)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 140, 371, 251))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gap = QtGui.QSpinBox(self.groupBox_2)
        self.gap.setEnabled(False)
        self.gap.setGeometry(QtCore.QRect(80, 20, 51, 20))
        self.gap.setMinimum(2)
        self.gap.setMaximum(100)
        self.gap.setSingleStep(2)
        self.gap.setObjectName(_fromUtf8("gap"))
        self.label_4 = QtGui.QLabel(self.groupBox_2)
        self.label_4.setGeometry(QtCore.QRect(13, 22, 57, 14))
        self.label_4.setObjectName(_fromUtf8("label_4"))

        self.retranslateUi(FormSacks)
        QtCore.QMetaObject.connectSlotsByName(FormSacks)

    def retranslateUi(self, FormSacks):
        FormSacks.setWindowTitle(_translate("FormSacks", "Form", None))
        self.groupBox.setTitle(_translate("FormSacks", "Primary", None))
        self.label.setText(_translate("FormSacks", "Dataset", None))
        self.label_2.setText(_translate("FormSacks", "Minimum", None))
        self.label_3.setText(_translate("FormSacks", "Maximum", None))
        self.dataset.setItemText(0, _translate("FormSacks", "Primes", None))
        self.dataset.setItemText(1, _translate("FormSacks", "Prime Pairs", None))
        self.groupBox_2.setTitle(_translate("FormSacks", "Extras", None))
        self.label_4.setText(_translate("FormSacks", "Pair Gap", None))

