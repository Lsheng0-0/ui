# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ranking_list.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget

from ui.tooltip.demo import ToolTip

background = 'background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 174, 254, 255),' \
             'stop:1 rgba(149, 209, 214, 255)) '
style = 'background-color:rgb(247, 248, 255)'
style2 = 'background-color:rgb(237, 238, 255)'

ranking_list_Bottom_td_1 = []
ranking_list_Bottom_td_1_Hor = []
ranking_list_Bottom_td_1_no = []
ranking_list_Bottom_td_1_choice = []
ranking_list_Bottom_td_1_name = []
ranking_list_Bottom_td_1_play = []
ranking_list_Bottom_td_1_download = []


class Ui_ranking_list(QWidget):
    def setupUi(self, ranking_list,na,so_na):
        ranking_list_Bottom_td_1.clear()
        ranking_list_Bottom_td_1_Hor.clear()
        ranking_list_Bottom_td_1_no.clear()
        ranking_list_Bottom_td_1_choice.clear()
        ranking_list_Bottom_td_1_name.clear()
        ranking_list_Bottom_td_1_play.clear()
        ranking_list_Bottom_td_1_download.clear()
        
        ranking_list.setObjectName("ranking_list")
        ranking_list.resize(800, 246)
        ranking_list.setMinimumSize(QtCore.QSize(700, 0))
        ranking_list.setMaximumSize(QtCore.QSize(900, 16777215))
        ranking_list.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.verticalLayout = QtWidgets.QVBoxLayout(ranking_list)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ranking_list_Top = QtWidgets.QFrame(ranking_list)
        self.ranking_list_Top.setMinimumSize(QtCore.QSize(800, 100))
        self.ranking_list_Top.setMaximumSize(QtCore.QSize(16777215, 100))
        self.ranking_list_Top.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ranking_list_Top.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ranking_list_Top.setObjectName("ranking_list_Top")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.ranking_list_Top)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.ranking_list_Top_na_Label = QtWidgets.QLabel(self.ranking_list_Top)
        self.ranking_list_Top_na_Label.setMinimumSize(QtCore.QSize(300, 80))
        self.ranking_list_Top_na_Label.setMaximumSize(QtCore.QSize(300, 80))
        font = QtGui.QFont()
        font.setFamily("二字元风波泡泡简")
        font.setPointSize(50)
        font.setBold(False)
        font.setWeight(50)
        self.ranking_list_Top_na_Label.setFont(font)
        self.ranking_list_Top_na_Label.setStyleSheet(
                "padding-right:50px;\n"
                "color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(223, 125, 255, 255), stop:1 rgba("
                "130, 186, "
                "255, 255));"
        
        )
        self.ranking_list_Top_na_Label.setObjectName("ranking_list_Top_na_Label")
        self.verticalLayout_2.addWidget(self.ranking_list_Top_na_Label)
        self.verticalLayout.addWidget(self.ranking_list_Top)
        self.ranking_list_Bottom = QtWidgets.QFrame(ranking_list)
        self.ranking_list_Bottom.setStyleSheet(
                "#song_list_bottom{border: 1px solid  qlineargradient(spread:pad, "
                "x1:0, y1:0, x2:1, y2:1, stop:0 rgba(247, 141, 147, 255), "
                "stop:0.965909 rgba(141, 193, 255, 255))}\n "
                "QPushButton{\n"
                "    border:none;\n"
                "    color:rgb(98, 98, 98);\n"
                "    text-align :center;\n"
                "    font: 9pt \"本墨字语\";\n"
                "}\n"
                "QPushButton:hover{  \n"
                "    padding-bottom:2px; \n"
                "}\n"
                "QLabel{\n"
                "    font: 9pt \"本墨字语\";\n"
                "}"
        )
        self.ranking_list_Bottom.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ranking_list_Bottom.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ranking_list_Bottom.setObjectName("ranking_list_Bottom")
        self.verticalLayout_song_list_bottom = QtWidgets.QVBoxLayout(self.ranking_list_Bottom)
        self.verticalLayout_song_list_bottom.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_song_list_bottom.setSpacing(0)
        self.verticalLayout_song_list_bottom.setObjectName("verticalLayout_song_list_bottom")
        self.ranking_list_Bottom_td_0 = QtWidgets.QFrame(self.ranking_list_Bottom)
        self.ranking_list_Bottom_td_0.setMinimumSize(QtCore.QSize(0, 40))
        self.ranking_list_Bottom_td_0.setMaximumSize(QtCore.QSize(16777215, 40))
        self.ranking_list_Bottom_td_0.setStyleSheet("")
        self.ranking_list_Bottom_td_0.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ranking_list_Bottom_td_0.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ranking_list_Bottom_td_0.setObjectName("ranking_list_Bottom_td_0")
        self.horizontalLayout_frame_song_list_list_bottom_lable = QtWidgets.QHBoxLayout(self.ranking_list_Bottom_td_0)
        self.horizontalLayout_frame_song_list_list_bottom_lable.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_frame_song_list_list_bottom_lable.setSpacing(0)
        self.horizontalLayout_frame_song_list_list_bottom_lable.setObjectName(
                "horizontalLayout_frame_song_list_list_bottom_lable"
        )
        self.ranking_list_Bottom_td_0_xuhao = QtWidgets.QLabel(self.ranking_list_Bottom_td_0)
        self.ranking_list_Bottom_td_0_xuhao.setMinimumSize(QtCore.QSize(90, 40))
        self.ranking_list_Bottom_td_0_xuhao.setMaximumSize(QtCore.QSize(90, 40))
        self.ranking_list_Bottom_td_0_xuhao.setStyleSheet("")
        self.ranking_list_Bottom_td_0_xuhao.setAlignment(QtCore.Qt.AlignCenter)
        self.ranking_list_Bottom_td_0_xuhao.setObjectName("ranking_list_Bottom_td_0_xuhao")
        self.horizontalLayout_frame_song_list_list_bottom_lable.addWidget(self.ranking_list_Bottom_td_0_xuhao)
        self.ranking_list_Bottom_td_0_so_name = QtWidgets.QPushButton(self.ranking_list_Bottom_td_0)
        self.ranking_list_Bottom_td_0_so_name.setMinimumSize(QtCore.QSize(440, 40))
        self.ranking_list_Bottom_td_0_so_name.setMaximumSize(QtCore.QSize(440, 40))
        self.ranking_list_Bottom_td_0_so_name.setStyleSheet("text-align :left;")
        self.ranking_list_Bottom_td_0_so_name.setObjectName("ranking_list_Bottom_td_0_so_name")
        self.horizontalLayout_frame_song_list_list_bottom_lable.addWidget(self.ranking_list_Bottom_td_0_so_name)
        self.ranking_list_Bottom_td_0_Bt = QtWidgets.QFrame(self.ranking_list_Bottom_td_0)
        self.ranking_list_Bottom_td_0_Bt.setMinimumSize(QtCore.QSize(340, 40))
        self.ranking_list_Bottom_td_0_Bt.setMaximumSize(QtCore.QSize(340, 40))
        self.ranking_list_Bottom_td_0_Bt.setStyleSheet(
                "QPushButton{\n"
                "border:none;\n"
                "    border-radius:10px;\n"
                "    color: rgb(255, 255, 255);\n"
                "    font: 10pt \"本墨字语\";\n"
                "%s;\n "
                "border: 1px solid  qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0 rgba(161, 174, 255, "
                "255), "
                "stop:0.863636 rgba(74, 129, 230, 255));\n "
                "}\n"
                "QPushButton:hover{  \n"
                "    color: rgb(213, 8, 8);\n"
                "    padding-bottom:3px; \n"
                "}\n"
                "QPushButton:focus {\n"
                "      color: rgb(255, 255, 255);\n"
                "      outline: 0px;\n"
                "    }\n"
                "QPushButton:pressed{\n"
                "    background-color: rgb(200, 200, 200);\n"
                "    color: rgb(255, 149, 0);\n"
                "}\n" % background
        )
        self.ranking_list_Bottom_td_0_Bt.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ranking_list_Bottom_td_0_Bt.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ranking_list_Bottom_td_0_Bt.setObjectName("ranking_list_Bottom_td_0_Bt")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.ranking_list_Bottom_td_0_Bt)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(7)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.ranking_list_Bottom_td_0_Bt_play = QtWidgets.QPushButton(self.ranking_list_Bottom_td_0_Bt)
        self.ranking_list_Bottom_td_0_Bt_play.setMinimumSize(QtCore.QSize(0, 25))
        self.ranking_list_Bottom_td_0_Bt_play.setMaximumSize(QtCore.QSize(90, 25))
        self.ranking_list_Bottom_td_0_Bt_play.setStyleSheet("")
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(":/icon/icon/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ranking_list_Bottom_td_0_Bt_play.setIcon(self.icon)
        self.ranking_list_Bottom_td_0_Bt_play.setIconSize(QtCore.QSize(12, 12))
        self.ranking_list_Bottom_td_0_Bt_play.setObjectName("ranking_list_Bottom_td_0_Bt_play_{}".format(na))
        self.horizontalLayout_4.addWidget(self.ranking_list_Bottom_td_0_Bt_play)
        self.ranking_list_Bottom_td_0_Bt_collect = QtWidgets.QPushButton(self.ranking_list_Bottom_td_0_Bt)
        self.ranking_list_Bottom_td_0_Bt_collect.setMinimumSize(QtCore.QSize(0, 25))
        self.ranking_list_Bottom_td_0_Bt_collect.setMaximumSize(QtCore.QSize(90, 25))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icon/icon/add_1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ranking_list_Bottom_td_0_Bt_collect.setIcon(icon1)
        self.ranking_list_Bottom_td_0_Bt_collect.setIconSize(QtCore.QSize(20, 20))
        self.ranking_list_Bottom_td_0_Bt_collect.setObjectName("ranking_list_Bottom_td_0_Bt_collect_{}".format(na))
        self.horizontalLayout_4.addWidget(self.ranking_list_Bottom_td_0_Bt_collect)
        self.ranking_list_Bottom_td_0_Bt_load = QtWidgets.QPushButton(self.ranking_list_Bottom_td_0_Bt)
        self.ranking_list_Bottom_td_0_Bt_load.setMinimumSize(QtCore.QSize(0, 25))
        self.ranking_list_Bottom_td_0_Bt_load.setMaximumSize(QtCore.QSize(90, 25))
        self.icon2 = QtGui.QIcon()
        self.icon2.addPixmap(QtGui.QPixmap(":/icon/icon/download.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ranking_list_Bottom_td_0_Bt_load.setIcon(self.icon2)
        self.ranking_list_Bottom_td_0_Bt_load.setObjectName("ranking_list_Bottom_td_0_Bt_load_{}".format(na))
        self.horizontalLayout_4.addWidget(self.ranking_list_Bottom_td_0_Bt_load)
        self.horizontalLayout_frame_song_list_list_bottom_lable.addWidget(self.ranking_list_Bottom_td_0_Bt)
        self.verticalLayout_song_list_bottom.addWidget(self.ranking_list_Bottom_td_0)
        
        spacerItem = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_song_list_bottom.addItem(spacerItem)
        self.verticalLayout.addWidget(self.ranking_list_Bottom)
        for i in range(len(so_na)):
            if (i + 1) % 2 == 0:
                style_tr = style
            else:
                style_tr = style2
            self.table_td(na, i, style_tr)
            ranking_list_Bottom_td_1_name[i].clicked.connect(ranking_list_Bottom_td_1_choice[i].click)
        
        self.retranslateUi(ranking_list,na, so_na)
        QtCore.QMetaObject.connectSlotsByName(ranking_list)
        
    
    def table_td(self, na, i, style_tr):
        
        self.ranking_list_Bottom_td_1 = QtWidgets.QFrame(self.ranking_list_Bottom)
        self.ranking_list_Bottom_td_1.setMinimumSize(QtCore.QSize(0, 40))
        self.ranking_list_Bottom_td_1.setMaximumSize(QtCore.QSize(16777215, 40))
        self.ranking_list_Bottom_td_1.setStyleSheet(
                "QFrame,QLabel,QPushButton,QRadioButton{border:none;%s;}\n"
                "QPushButton:hover{color: qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0 rgba(162, 179, "
                "255, 255), stop:1 rgba(144, 228, 137, 255));\n "
                "}" % style_tr
        )
        self.ranking_list_Bottom_td_1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ranking_list_Bottom_td_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ranking_list_Bottom_td_1.setObjectName("ranking_list_Bottom_td_{}".format(na + str(i + 1)))  # i = 1
        ranking_list_Bottom_td_1.append(self.ranking_list_Bottom_td_1)
        
        self.ranking_list_Bottom_td_1_Hor = QtWidgets.QHBoxLayout(ranking_list_Bottom_td_1[i])
        self.ranking_list_Bottom_td_1_Hor.setContentsMargins(0, 0, 0, 0)
        self.ranking_list_Bottom_td_1_Hor.setSpacing(0)
        self.ranking_list_Bottom_td_1_Hor.setObjectName("ranking_list_Bottom_td_{}_Hor".format(na + str(i + 1)))
        ranking_list_Bottom_td_1_Hor.append(self.ranking_list_Bottom_td_1_Hor)
        
        self.ranking_list_Bottom_td_1_no = QtWidgets.QLabel(ranking_list_Bottom_td_1[i])
        self.ranking_list_Bottom_td_1_no.setMinimumSize(QtCore.QSize(40, 40))
        self.ranking_list_Bottom_td_1_no.setMaximumSize(QtCore.QSize(40, 40))
        self.ranking_list_Bottom_td_1_no.setStyleSheet("")
        self.ranking_list_Bottom_td_1_no.setAlignment(QtCore.Qt.AlignCenter)
        self.ranking_list_Bottom_td_1_no.setObjectName("ranking_list_Bottom_td_{}_no".format(i))
        ranking_list_Bottom_td_1_no.append(self.ranking_list_Bottom_td_1_no)
        ranking_list_Bottom_td_1_Hor[i].addWidget(ranking_list_Bottom_td_1_no[i])
        
        self.ranking_list_Bottom_td_1_choice = QtWidgets.QRadioButton(ranking_list_Bottom_td_1[i])
        self.ranking_list_Bottom_td_1_choice.setMinimumSize(QtCore.QSize(40, 40))
        self.ranking_list_Bottom_td_1_choice.setMaximumSize(QtCore.QSize(40, 40))
        self.ranking_list_Bottom_td_1_choice.setText("")
        self.ranking_list_Bottom_td_1_choice.setChecked(True)
        self.ranking_list_Bottom_td_1_choice.setObjectName("ranking_list_Bottom_td_{}_choice".format(na + str(i + 1)))
        ranking_list_Bottom_td_1_choice.append(self.ranking_list_Bottom_td_1_choice)
        ranking_list_Bottom_td_1_Hor[i].addWidget(ranking_list_Bottom_td_1_choice[i])
        
        self.ranking_list_Bottom_td_1_name = QtWidgets.QPushButton(ranking_list_Bottom_td_1[i])
        self.ranking_list_Bottom_td_1_name.setMinimumSize(QtCore.QSize(540, 40))
        self.ranking_list_Bottom_td_1_name.setMaximumSize(QtCore.QSize(540, 40))
        self.ranking_list_Bottom_td_1_name.setStyleSheet("text-align :left;")
        self.ranking_list_Bottom_td_1_name.setObjectName("ranking_list_Bottom_td_{}_name".format(na + str(i + 1)))
        ranking_list_Bottom_td_1_name.append(self.ranking_list_Bottom_td_1_name)
        ranking_list_Bottom_td_1_Hor[i].addWidget(ranking_list_Bottom_td_1_name[i])
        
        self.ranking_list_Bottom_td_1_play = QtWidgets.QPushButton(ranking_list_Bottom_td_1[i])
        self.ranking_list_Bottom_td_1_play.setMinimumSize(QtCore.QSize(40, 40))
        self.ranking_list_Bottom_td_1_play.setMaximumSize(QtCore.QSize(40, 40))
        self.ranking_list_Bottom_td_1_play.setText("")
        self.ranking_list_Bottom_td_1_play.setIcon(self.icon)
        self.ranking_list_Bottom_td_1_play.setIconSize(QtCore.QSize(13, 13))
        self.ranking_list_Bottom_td_1_play.setObjectName("ranking_list_Bottom_td_{}_play".format(na + str(i + 1)))
        ranking_list_Bottom_td_1_play.append(self.ranking_list_Bottom_td_1_play)
        ranking_list_Bottom_td_1_Hor[i].addWidget(ranking_list_Bottom_td_1_play[i])
        
        self.ranking_list_Bottom_td_1_download = QtWidgets.QPushButton(ranking_list_Bottom_td_1[i])
        self.ranking_list_Bottom_td_1_download.setMinimumSize(QtCore.QSize(40, 40))
        self.ranking_list_Bottom_td_1_download.setMaximumSize(QtCore.QSize(40, 40))
        self.ranking_list_Bottom_td_1_download.setText("")
        self.ranking_list_Bottom_td_1_download.setIcon(self.icon2)
        self.ranking_list_Bottom_td_1_download.setIconSize(QtCore.QSize(18, 18))
        self.ranking_list_Bottom_td_1_download.setObjectName(
            "ranking_list_Bottom_td_{}_download".format(na + str(i + 1))
            )
        ranking_list_Bottom_td_1_download.append(self.ranking_list_Bottom_td_1_download)
        ranking_list_Bottom_td_1_Hor[i].addWidget(self.ranking_list_Bottom_td_1_download)
        self.verticalLayout_song_list_bottom.addWidget(self.ranking_list_Bottom_td_1)
    
    def retranslateUi(self, ranking_list,na, so_na):
        global so_br_na
        _translate = QtCore.QCoreApplication.translate
        ranking_list.setWindowTitle(_translate("ranking_list", "Form"))
        if na == 'soar':
            so_br_na = '飙升榜'
        elif na == 'hotsong':
            so_br_na = '热歌榜'
        elif na == 'newsong':
            so_br_na = '新歌榜'
            
        self.ranking_list_Top_na_Label.setText(_translate("ranking_list", "{}".format(so_br_na)))
        self.ranking_list_Bottom_td_0_xuhao.setText(_translate("ranking_list", "序号"))
        self.ranking_list_Bottom_td_0_so_name.setText(_translate("ranking_list", "歌曲"))
        self.ranking_list_Bottom_td_0_Bt_play.setText(_translate("ranking_list", "播放列表"))
        self.ranking_list_Bottom_td_0_Bt_collect.setText(_translate("ranking_list", "收藏歌单"))
        self.ranking_list_Bottom_td_0_Bt_load.setText(_translate("ranking_list", "下载列表"))
        
        for i in range(len(ranking_list_Bottom_td_1_no)):
            ranking_list_Bottom_td_1_no[i].setText(_translate("ranking_list", "{}".format(i+1)))
            ranking_list_Bottom_td_1_name[i].setToolTip(
                _translate(
                    "ranking_list","<html><head/><body><p><span style=\" font-size:8pt; font-family:\'本墨字语\'\">{}</span></p></body></html>".format(
                            so_na[i])
                    )
                )
            ranking_list_Bottom_td_1_name[i].setText(_translate("ranking_list", "{}".format(so_na[i])))


import pic.icon_rc
