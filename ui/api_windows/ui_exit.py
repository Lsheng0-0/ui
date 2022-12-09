# -*- coding: UTF-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from ui.exit import Ui_exit


class ui_exit(QWidget, Ui_exit):
    def __init__(self):
        super(ui_exit, self).__init__()
        self.setupUi(self)
        # 将UI界面布局到Demo上；
        # 初始化
        self.setAttribute(Qt.WA_TranslucentBackground)  # 窗体背景透明
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)  # 窗口置顶，无边框，在任务栏不显示图标
        self.setWindowOpacity(1)  # 设置窗口透明度