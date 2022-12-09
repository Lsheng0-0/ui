# -*- coding: UTF-8 -*-
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QDialog
from ui.mp3 import Ui_mp3


class ui_mp3(QDialog, Ui_mp3):
    mp3_play_bt = pyqtSignal()
    mp3_exit_bt = pyqtSignal()
    mp3_last_bt = pyqtSignal()
    mp3_next_bt = pyqtSignal()
    mp3_pattern_bt = pyqtSignal()
    
    def __init__(self, parent=None):
        super(ui_mp3, self).__init__(parent)
        self.setupUi(self)
        # 将UI界面布局到Demo上；
        # 初始化
        self.move(1580, 960)
        
        self.setAttribute(Qt.WA_TranslucentBackground)  # 窗体背景透明
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setWindowOpacity(0.98)  # 设置窗口透明度
        self.mp3_sign = 0
        self.mp3_information_logo_Bt.clicked.connect(lambda: self.bt_page_mp3_sign())  # 页面切换
        self.mp3_information_down_Bt.clicked.connect(lambda: self.bt_page_ini_sign())  # 页面切换
        
        # mp3
        self.mp3_player_play_Bt.clicked.connect(lambda: self.mp3_play_sign())  # MP3播放按钮信号槽
        self.mp3_player_last_Bt.clicked.connect(lambda: self.mp3_last_sign())  # MP3上一首按钮信号槽
        self.mp3_player_next_Bt.clicked.connect(lambda: self.mp3_next_sign())  # MP3下一首按钮信号槽
        self.mp3_player_pattern_Bt.clicked.connect(lambda: self.mp3_pattern_sign())  # MP3播放顺序按钮信号槽
        self.mp3_setting_Bt.clicked.connect(lambda: self.mp3_exit_sign())  # MP3退出按钮信号槽

        
        self.m_flag = False
    

    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标
    
    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()
    
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))
    
    '''底部两个界面'''
    
    def sWidget_pl(self, p):
        try:
            if self.so_serial == 1:
                self.ing_mc.close()
        except:
            pass
        self.mp3_SW.setCurrentIndex(p)
    
    def bt_page_mp3_sign(self):
        self.sWidget_pl(1)
    
    def bt_page_ini_sign(self):
        self.sWidget_pl(0)
    
    def mp3_play_sign(self):
        self.mp3_play_bt.emit()
    
    def mp3_exit_sign(self):
        self.close()
    
    def mp3_last_sign(self):
        self.mp3_last_bt.emit()
    
    def mp3_next_sign(self):
        self.mp3_next_bt.emit()
    
    def mp3_pattern_sign(self):
        self.mp3_pattern_bt.emit()
