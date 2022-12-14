# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'exit.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_exit(object):
    def setupUi(self, exit):
        exit.setObjectName("exit")
        exit.resize(376, 246)
        exit.setStyleSheet("exit:{\n"
"opacity :1;\n"
"background-color: rgba(255, 255, 255, 0);}\n"
"")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(exit)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.frame_exit_main = QtWidgets.QFrame(exit)
        self.frame_exit_main.setMinimumSize(QtCore.QSize(358, 228))
        self.frame_exit_main.setMaximumSize(QtCore.QSize(358, 228))
        self.frame_exit_main.setStyleSheet("\n"
"#frame_exit_main{   \n"
"border:none;\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 174, 254, 255), stop:1 rgba(149, 209, 214, 255));\n"
" border-top:1px solid darkGray;\n"
"    border-bottom:1px solid darkGray;\n"
"    border-right:1px solid darkGray;\n"
"    border-left:1px solid darkGray;\n"
"    border-top-right-radius:10px;\n"
"    border-bottom-right-radius:10px;\n"
"    border-top-left-radius:10px;\n"
"    border-bottom-left-radius:10px;;}\n"
"")
        self.frame_exit_main.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_exit_main.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_exit_main.setObjectName("frame_exit_main")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_exit_main)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_exit = QtWidgets.QFrame(self.frame_exit_main)
        self.frame_exit.setStyleSheet("")
        self.frame_exit.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_exit.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_exit.setObjectName("frame_exit")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_exit)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_exit_2 = QtWidgets.QFrame(self.frame_exit)
        self.frame_exit_2.setMinimumSize(QtCore.QSize(0, 30))
        self.frame_exit_2.setMaximumSize(QtCore.QSize(16777215, 30))
        self.frame_exit_2.setStyleSheet("border:none;\n"
"border-bottom: 1px solid  rgb(161, 161, 161); \n"
"border-radius:10px;")
        self.frame_exit_2.setObjectName("frame_exit_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_exit_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(340, 4, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButton_exit_2_2 = QtWidgets.QPushButton(self.frame_exit_2)
        self.pushButton_exit_2_2.setMinimumSize(QtCore.QSize(20, 20))
        self.pushButton_exit_2_2.setMaximumSize(QtCore.QSize(20, 20))
        self.pushButton_exit_2_2.setStyleSheet("QPushButton{border:none;border-radius:12px;color: rgb(255, 255, 255);border-radius:8px; } QPushButton:hover{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 174, 254, 255), stop:1 rgba(149, 209, 214, 255));\n"
"}\n"
"\n"
"")
        self.pushButton_exit_2_2.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/icon/exit_black.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_exit_2_2.setIcon(icon)
        self.pushButton_exit_2_2.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_exit_2_2.setObjectName("pushButton_exit_2_2")
        self.horizontalLayout_2.addWidget(self.pushButton_exit_2_2)
        self.verticalLayout_2.addWidget(self.frame_exit_2, 0, QtCore.Qt.AlignTop)
        self.frame_label_exit = QtWidgets.QFrame(self.frame_exit)
        self.frame_label_exit.setMinimumSize(QtCore.QSize(330, 120))
        self.frame_label_exit.setMaximumSize(QtCore.QSize(330, 120))
        self.frame_label_exit.setStyleSheet("#frame_label_exit{;\n"
"    background-color: rgb(255, 255, 255);\n"
"border-radius:15px}")
        self.frame_label_exit.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_label_exit.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_label_exit.setObjectName("frame_label_exit")
        self.verticalLayout_exit = QtWidgets.QVBoxLayout(self.frame_label_exit)
        self.verticalLayout_exit.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_exit.setSpacing(0)
        self.verticalLayout_exit.setObjectName("verticalLayout_exit")
        self.label_exit = QtWidgets.QLabel(self.frame_label_exit)
        self.label_exit.setMinimumSize(QtCore.QSize(0, 60))
        self.label_exit.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("????????????")
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.label_exit.setFont(font)
        self.label_exit.setStyleSheet("padding-top:15px")
        self.label_exit.setAlignment(QtCore.Qt.AlignCenter)
        self.label_exit.setObjectName("label_exit")
        self.verticalLayout_exit.addWidget(self.label_exit)
        self.frame_exit_3 = QtWidgets.QFrame(self.frame_label_exit)
        self.frame_exit_3.setMinimumSize(QtCore.QSize(0, 40))
        self.frame_exit_3.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frame_exit_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_exit_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_exit_3.setObjectName("frame_exit_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_exit_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.radioButton_exit = QtWidgets.QRadioButton(self.frame_exit_3)
        self.radioButton_exit.setMinimumSize(QtCore.QSize(0, 35))
        self.radioButton_exit.setMaximumSize(QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setFamily("????????????")
        font.setPointSize(10)
        self.radioButton_exit.setFont(font)
        self.radioButton_exit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.radioButton_exit.setStyleSheet("")
        self.radioButton_exit.setObjectName("radioButton_exit")
        self.horizontalLayout_3.addWidget(self.radioButton_exit, 0, QtCore.Qt.AlignHCenter)
        self.radioButton_exit_2 = QtWidgets.QRadioButton(self.frame_exit_3)
        self.radioButton_exit_2.setMinimumSize(QtCore.QSize(0, 35))
        self.radioButton_exit_2.setMaximumSize(QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setFamily("????????????")
        font.setPointSize(10)
        self.radioButton_exit_2.setFont(font)
        self.radioButton_exit_2.setStyleSheet("")
        self.radioButton_exit_2.setChecked(True)
        self.radioButton_exit_2.setObjectName("radioButton_exit_2")
        self.horizontalLayout_3.addWidget(self.radioButton_exit_2, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_exit.addWidget(self.frame_exit_3, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_2.addWidget(self.frame_label_exit, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addWidget(self.frame_exit)
        self.widget_exit = QtWidgets.QWidget(self.frame_exit_main)
        self.widget_exit.setMinimumSize(QtCore.QSize(0, 50))
        self.widget_exit.setMaximumSize(QtCore.QSize(16777215, 50))
        self.widget_exit.setStyleSheet("#widget_exit{border:none;border-radius:10px;\n"
"border-top: 1px solid  rgb(161, 161, 161); }")
        self.widget_exit.setObjectName("widget_exit")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_exit)
        self.horizontalLayout.setContentsMargins(5, 0, 5, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.checkBox_exit = QtWidgets.QCheckBox(self.widget_exit)
        self.checkBox_exit.setMinimumSize(QtCore.QSize(100, 0))
        self.checkBox_exit.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("????????????")
        font.setPointSize(9)
        self.checkBox_exit.setFont(font)
        self.checkBox_exit.setStyleSheet("")
        self.checkBox_exit.setObjectName("checkBox_exit")
        self.horizontalLayout.addWidget(self.checkBox_exit)
        self.pushButton_exit_ok = QtWidgets.QPushButton(self.widget_exit)
        self.pushButton_exit_ok.setMinimumSize(QtCore.QSize(100, 25))
        self.pushButton_exit_ok.setMaximumSize(QtCore.QSize(100, 25))
        font = QtGui.QFont()
        font.setFamily("????????????")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_exit_ok.setFont(font)
        self.pushButton_exit_ok.setStyleSheet("QPushButton{;color: rgb(255, 255, 255);border-radius:8px;border: 1px solid  rgb(53, 53, 53); } QPushButton:hover{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 174, 254, 255), stop:1 rgba(149, 209, 214, 255));\n"
"}\n"
"")
        self.pushButton_exit_ok.setObjectName("pushButton_exit_ok")
        self.horizontalLayout.addWidget(self.pushButton_exit_ok)
        self.verticalLayout.addWidget(self.widget_exit)
        self.horizontalLayout_4.addWidget(self.frame_exit_main)

        self.retranslateUi(exit)
        QtCore.QMetaObject.connectSlotsByName(exit)

    def retranslateUi(self, exit):
        _translate = QtCore.QCoreApplication.translate
        exit.setWindowTitle(_translate("exit", "Form"))
        self.label_exit.setText(_translate("exit", "????????????"))
        self.radioButton_exit.setText(_translate("exit", "???????????????    "))
        self.radioButton_exit_2.setText(_translate("exit", "??????????????????"))
        self.checkBox_exit.setText(_translate("exit", "????????????"))
        self.pushButton_exit_ok.setText(_translate("exit", "??????"))
import pic.icon_rc
