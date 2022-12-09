# -*- coding: UTF-8 -*-
from collections import defaultdict

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

from ui.template.so_list import Ui_so_li


class ui_grid_li(QWidget, Ui_so_li):
    def __init__(self, list_na, im_path, alt, inf_int, song_name):
        super(ui_grid_li, self).__init__()
        self.setupUi(self, list_na, list_na.split('_')[0], im_path, alt, inf_int, song_name)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)  # 窗口置顶，无边框，在任务栏不显示图标