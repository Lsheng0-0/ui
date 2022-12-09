# -*- coding: UTF-8 -*-
import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QFontMetrics, QPainter, QPixmap, QColor
from PyQt5.QtWidgets import QWidget


class ScrollTextWindow(QWidget):
    """ 滚动字幕 """
    
    def __init__(self, songerName, songName, fong_size, interval, parent=None):
        super().__init__(parent)
        self.songName = songName
        self.songerName = songerName
        # 实例化定时器
        self.timer = QTimer(self)
        # 设置刷新时间和移动距离
        self.timeStep = 30
        self.moveStep = 1
        self.songCurrentIndex = 0
        self.songerCurrentIndex = 0
        # 设置字符串溢出标志位
        self.isSongNameAllOut = False
        self.isSongerNameAllOut = False
        # 设置两段字符串之间留白的宽度
        self.spacing = 30
        self.fong_size = fong_size
        self.interval = interval
        # 初始化界面
        self.initWidget()
        
    def initWidget(self):
        """ 初始化界面 """
        self.setFixedHeight(40)
        # self.setAttribute(Qt.WA_StyledBackground)
        # 调整窗口宽度
        self.adjustWindowWidth()
        # 初始化定时器
        self.timer.setInterval(self.timeStep)
        self.timer.timeout.connect(self.updateIndex)
        # 只要有一个字符串宽度大于窗口宽度就开启滚动：
        if self.isSongerNameTooLong or self.isSongNameTooLong:
            self.timer.start()
    
    def getTextWidth(self):
        """ 计算文本的总宽度 """
        songFontMetrics = QFontMetrics(QFont('微软雅黑', self.fong_size, 400))
        self.songNameWidth = songFontMetrics.width(self.songName)
        songerFontMetrics = QFontMetrics(QFont('微软雅黑', self.fong_size, 500))
        self.songerNameWidth = songerFontMetrics.width(self.songerName)
    
    def adjustWindowWidth(self):
        """ 根据字符串长度调整窗口宽度 """
        self.getTextWidth()
        maxWidth = max(self.songNameWidth, self.songerNameWidth)
        # 判断是否有字符串宽度超过窗口的最大宽度
        self.isSongNameTooLong = self.songNameWidth > 150
        self.isSongerNameTooLong = self.songerNameWidth > 150
        # 设置窗口的宽度
        self.setFixedWidth(min(maxWidth, 250))
    
    def updateIndex(self):
        """ 更新下标 """
        self.update()
        self.songCurrentIndex += 1
        self.songerCurrentIndex += 1
        # 设置下标重置条件
        resetSongIndexCond = self.songCurrentIndex * \
                             self.moveStep >= self.songNameWidth + self.spacing * self.isSongNameAllOut
        resetSongerIndexCond = self.songerCurrentIndex * \
                               self.moveStep >= self.songerNameWidth + self.spacing * self.isSongerNameAllOut
        # 只要条件满足就要重置下标并将字符串溢出置位，保证在字符串溢出后不会因为留出的空白而发生跳变
        if resetSongIndexCond:
            self.songCurrentIndex = 0
            self.isSongNameAllOut = True
        if resetSongerIndexCond:
            self.songerCurrentIndex = 0
            self.isSongerNameAllOut = True
        
    def paintEvent(self, e):
        """ 绘制文本 """
        # super().paintEvent(e)
        painter = QPainter(self)
        painter.setPen(QColor(76, 76, 76))
        # 绘制歌名
        painter.setFont(QFont('微软雅黑', self.fong_size, 400))
        if self.isSongNameTooLong:
            # 实际上绘制了两段完整的字符串
            # 从负的横坐标开始绘制第一段字符串
            painter.drawText(
                    self.spacing * self.isSongNameAllOut - self.moveStep *
                    self.songCurrentIndex, 15, self.songName
            )
            # 绘制第二段字符串
            painter.drawText(
                    self.songNameWidth - self.moveStep * self.songCurrentIndex +
                    self.spacing * (1 + self.isSongNameAllOut), 15, self.songName
            )
        else:
            painter.drawText(0, 15, self.songName)
        # 绘制歌手名
        painter.setFont(QFont('微软雅黑', self.fong_size, 500))
        if self.isSongerNameTooLong:
            painter.drawText(
                    self.spacing * self.isSongerNameAllOut - self.moveStep *
                    self.songerCurrentIndex, 15+ self.interval, self.songerName
            )
            painter.drawText(
                    self.songerNameWidth - self.moveStep * self.songerCurrentIndex +
                    self.spacing * (1 + self.isSongerNameAllOut), 15+ self.interval, self.songerName
            )
        else:
            painter.drawText(0, 15+ self.interval, self.songerName)
