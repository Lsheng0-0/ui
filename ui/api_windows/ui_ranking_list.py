# -*- coding: UTF-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

from ui.template.ra_list import Ui_ranking_list


class Ui_ra_list(QWidget):
    def __init__(self, na, so_na):
        super(Ui_ra_list, self).__init__()
        self.rank = Ui_ranking_list()
        self.rank.setupUi(self, na, so_na)
        self.setAttribute(Qt.WA_TranslucentBackground)  # 窗体背景透明
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

