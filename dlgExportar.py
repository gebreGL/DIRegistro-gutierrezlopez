# Form implementation generated from reading ui file 'dlgExportar.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_dlgExportar(object):
    def setupUi(self, dlgExportar):
        dlgExportar.setObjectName("dlgExportar")
        dlgExportar.resize(399, 290)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("img/taller.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        dlgExportar.setWindowIcon(icon)
        self.pushButton = QtWidgets.QPushButton(dlgExportar)
        self.pushButton.setGeometry(QtCore.QRect(160, 230, 81, 31))
        self.pushButton.setObjectName("pushButton")
        self.lblPregunta = QtWidgets.QLabel(dlgExportar)
        self.lblPregunta.setGeometry(QtCore.QRect(70, 90, 261, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lblPregunta.setFont(font)
        self.lblPregunta.setObjectName("lblPregunta")
        self.lblInterrogacion = QtWidgets.QLabel(dlgExportar)
        self.lblInterrogacion.setGeometry(QtCore.QRect(180, 50, 41, 31))
        self.lblInterrogacion.setText("")
        self.lblInterrogacion.setPixmap(QtGui.QPixmap("img/interrogacion.png"))
        self.lblInterrogacion.setScaledContents(True)
        self.lblInterrogacion.setObjectName("lblInterrogacion")
        self.layoutWidget = QtWidgets.QWidget(dlgExportar)
        self.layoutWidget.setGeometry(QtCore.QRect(90, 160, 213, 25))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(49)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.checkBox = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.checkBox.setFont(font)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout.addWidget(self.checkBox)
        self.checkBox_2 = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox_2.setFont(font)
        self.checkBox_2.setObjectName("checkBox_2")
        self.horizontalLayout.addWidget(self.checkBox_2)

        self.retranslateUi(dlgExportar)
        QtCore.QMetaObject.connectSlotsByName(dlgExportar)

    def retranslateUi(self, dlgExportar):
        _translate = QtCore.QCoreApplication.translate
        dlgExportar.setWindowTitle(_translate("dlgExportar", "Exportar"))
        self.pushButton.setText(_translate("dlgExportar", "Aceptar"))
        self.lblPregunta.setText(_translate("dlgExportar", "Elija qu?? datos desea exportar :"))
        self.checkBox.setText(_translate("dlgExportar", "Clientes"))
        self.checkBox_2.setText(_translate("dlgExportar", "Coches"))
