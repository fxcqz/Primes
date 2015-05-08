# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'complex.ui'
#
# Created: Fri May  8 00:53:35 2015
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

class Ui_FormComplex(object):
    def setupUi(self, FormComplex):
        FormComplex.setObjectName(_fromUtf8("FormComplex"))
        FormComplex.resize(391, 411)
        self.groupBox = QtGui.QGroupBox(FormComplex)
        self.groupBox.setGeometry(QtCore.QRect(10, 20, 371, 111))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(20, 22, 50, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(16, 46, 54, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(13, 72, 57, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.dataset = QtGui.QComboBox(self.groupBox)
        self.dataset.setGeometry(QtCore.QRect(80, 20, 101, 20))
        self.dataset.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.dataset.setObjectName(_fromUtf8("dataset"))
        self.dataset.addItem(_fromUtf8(""))
        self.min_ = QtGui.QLineEdit(self.groupBox)
        self.min_.setGeometry(QtCore.QRect(80, 46, 101, 20))
        self.min_.setObjectName(_fromUtf8("min_"))
        self.max_ = QtGui.QLineEdit(self.groupBox)
        self.max_.setGeometry(QtCore.QRect(80, 72, 101, 20))
        self.max_.setObjectName(_fromUtf8("max_"))
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(200, 48, 71, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(200, 70, 161, 16))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_7 = QtGui.QLabel(self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(200, 84, 161, 16))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.groupBox_2 = QtGui.QGroupBox(FormComplex)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 140, 371, 251))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))

        self.retranslateUi(FormComplex)
        QtCore.QMetaObject.connectSlotsByName(FormComplex)

    def retranslateUi(self, FormComplex):
        FormComplex.setWindowTitle(_translate("FormComplex", "Form", None))
        self.groupBox.setTitle(_translate("FormComplex", "Primary", None))
        self.label.setText(_translate("FormComplex", "Dataset", None))
        self.label_2.setText(_translate("FormComplex", "Minimum", None))
        self.label_3.setText(_translate("FormComplex", "Maximum", None))
        self.dataset.setItemText(0, _translate("FormComplex", "Gaussians", None))
        self.label_5.setText(_translate("FormComplex", "e.g.  1+2j", None))
        self.label_6.setText(_translate("FormComplex", "where 1 is real and 2", None))
        self.label_7.setText(_translate("FormComplex", "is imaginary", None))
        self.groupBox_2.setTitle(_translate("FormComplex", "Extras", None))

