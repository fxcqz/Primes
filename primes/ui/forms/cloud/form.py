# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cloud.ui'
#
# Created: Fri May  8 01:09:56 2015
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

class Ui_FormCloud(object):
    def setupUi(self, FormCloud):
        FormCloud.setObjectName(_fromUtf8("FormCloud"))
        FormCloud.resize(391, 411)
        self.groupBox = QtGui.QGroupBox(FormCloud)
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
        self.dataset.addItem(_fromUtf8(""))
        self.groupBox_2 = QtGui.QGroupBox(FormCloud)
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
        self.mod_ = QtGui.QSpinBox(self.groupBox_2)
        self.mod_.setEnabled(True)
        self.mod_.setGeometry(QtCore.QRect(80, 48, 51, 20))
        self.mod_.setMinimum(2)
        self.mod_.setMaximum(100)
        self.mod_.setSingleStep(1)
        self.mod_.setProperty("value", 11)
        self.mod_.setObjectName(_fromUtf8("mod_"))
        self.label_5 = QtGui.QLabel(self.groupBox_2)
        self.label_5.setGeometry(QtCore.QRect(20, 50, 57, 14))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(self.groupBox_2)
        self.label_6.setGeometry(QtCore.QRect(22, 80, 57, 14))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.big_data = QtGui.QComboBox(self.groupBox_2)
        self.big_data.setEnabled(False)
        self.big_data.setGeometry(QtCore.QRect(80, 76, 111, 22))
        self.big_data.setObjectName(_fromUtf8("big_data"))
        self.big_data.addItem(_fromUtf8(""))
        self.big_data.addItem(_fromUtf8(""))
        self.big_data.addItem(_fromUtf8(""))
        self.big_data.addItem(_fromUtf8(""))

        self.retranslateUi(FormCloud)
        QtCore.QMetaObject.connectSlotsByName(FormCloud)

    def retranslateUi(self, FormCloud):
        FormCloud.setWindowTitle(_translate("FormCloud", "Form", None))
        self.groupBox.setTitle(_translate("FormCloud", "Primary", None))
        self.label.setText(_translate("FormCloud", "Dataset", None))
        self.label_2.setText(_translate("FormCloud", "Minimum", None))
        self.label_3.setText(_translate("FormCloud", "Maximum", None))
        self.dataset.setItemText(0, _translate("FormCloud", "Primes", None))
        self.dataset.setItemText(1, _translate("FormCloud", "Prime Pairs", None))
        self.dataset.setItemText(2, _translate("FormCloud", "Big Dataset", None))
        self.groupBox_2.setTitle(_translate("FormCloud", "Extras", None))
        self.label_4.setText(_translate("FormCloud", "Pair Gap", None))
        self.label_5.setText(_translate("FormCloud", "Modulo", None))
        self.label_6.setText(_translate("FormCloud", "Big Set", None))
        self.big_data.setItemText(0, _translate("FormCloud", "1 Million", None))
        self.big_data.setItemText(1, _translate("FormCloud", "2 Million", None))
        self.big_data.setItemText(2, _translate("FormCloud", "5 Million", None))
        self.big_data.setItemText(3, _translate("FormCloud", "10 Million", None))

