# !/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
stackedWidget_music_alone:
0 单曲歌词页面
stackedWidget_bottom :
0 音乐头像,名称

"""
import json
import os
import random
import sys
import threading
from collections import defaultdict
from time import sleep

from Lshengpackage.file.deal_file import file_fol
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import QUrl, QThread, pyqtSignal, QMutex, pyqtSlot, QTimer
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtWidgets import QMainWindow, QPushButton, QRadioButton, QLabel
from pachong.music.kg_mc import get_mp3_js, dload_image, red_cache, wr_js, obt_js, add_js_data, to_ini, down_load_mc, \
    red_js
from page.api_page import api_Page
from thread_mc.thread_mc import re_js_thread, re_so_ing_thread, add_list_thread, refresh_thread, \
    add_ranking_thread, set_songlist_page_Th, dload_mp3_thread
from ui.api_windows.ui_grid_list import ui_grid_li
from ui.api_windows.ui_ranking_list import Ui_ra_list
from ui.main_window import Ui_MainWindow
from ui.template.grid import Ui_grid
from ui.api_windows.ui_ing_list import ui_ing_mc
from ui.template.local_mc_list import Ui_local_mc_list
from ui.template.scroll_text import ScrollTextWindow

global gl_Last_so_P  # 上一个歌曲列表页
global gl_ing_url  # 当前音乐url
global gl_Page_and_num  # 播放的页面标签的第几个歌曲
global gl_So_na_lo  # 单个歌曲的名字，对应歌曲头像
global gl_All_list_play  # 全部播放的几个值

qmut_3 = QMutex()


class mc_p_Switch(QMainWindow, Ui_MainWindow):
    songInfo_label = pyqtSignal(str, str)
    
    def __init__(self):
        super(mc_p_Switch, self).__init__()
        # 将UI界面布局到Demo上；
        global gl_Page_and_num
        global gl_All_list_play
        global gl_Last_so_P
        global gl_ing_url
        gl_ing_url = None
        self.page_index_num = []
        self.page_last = 0
        self.lyric = []
        self.so_src_list = []
        self.ra_list = defaultdict(list)
        self.so_list_P = defaultdict(list)
        self.mc_list = defaultdict(list)
        self.index = 0  # 主页第二次到任务页
        self.so_detail = 1  # 下拉页面主页面返回索引变量
        self.so_serial = 0  # 正在播放list列表
        gl_Last_so_P = None
        gl_Page_and_num = []
        gl_All_list_play = []
        
        self.api_P = api_Page()
        self.ing_mc = ui_ing_mc()
        
        self.ing_mc.ing_clean.connect(lambda: self.player_stop_setting())  # 清理列表
        self.ing_mc.src_list_sign.connect(self.get_src_list)  # 每次更新一下就传一次列表url的数据

    # 获取播放歌单信号值
    def get_src_list(self, src_list):
        self.so_src_list = src_list
    
    '''播放和暂停设置'''
    
    # 每一次停止都需要做的一些操作
    def player_stop_setting(self):
        global gl_So_na_lo
        global gl_Page_and_num
        global gl_ing_url
        if len(gl_Page_and_num) != 0:
            try:
                li = self.ing_mc.findChild(
                        QPushButton, "pushButton_ing_mc_so_name_{}".format(gl_So_na_lo)
                )
                li.setStyleSheet("color :rgb(0,0,0);text-align :left;")
            except:
                pass
            self.bt_pause_change_song(gl_Page_and_num[0], gl_Page_and_num[1])
            self.player.stop()
            gl_Page_and_num = []
    
    # 暂停变化设置
    def bt_pause_change_song(self, grid_na, num):
        global gl_So_na_lo
        self.pushButton_bottom_play.setObjectName('play')
        self.pushButton_bottom_play.setIcon(QtGui.QIcon(':/icon/icon/play.png'))  # 设置图标
        try:
            # mp3 的暂停变化
            self.mp3.pushButton__mp3_button_1_download.setObjectName('play')
            self.mp3.pushButton__mp3_button_1_download.setIcon(QtGui.QIcon(':/icon/icon/play.png'))  # 设置图标
        except:
            pass
        try:
            bt_play_change = self.so_list_P[gl_Last_so_P][0].findChild(
                    QPushButton, "pushButton_song_list_bottom_play_{}_{}".format(grid_na, str(num))
            )
            bt_play_change.setIcon(QtGui.QIcon(':/icon/icon/play.png'))  # 设置图标
        
        except:  # 排行里歌单列表的播放图标，没加载就没有则不做处理
            try:
                bt_ranking_change = self.ra_list[gl_Last_so_P][0].findChild(
                        QPushButton, "ranking_list_Bottom_td_{}_play".format(
                                grid_na + str(num + 1)
                        )
                )
                bt_ranking_change.setIcon(QtGui.QIcon(':/icon/icon/play.png'))  # 设置图标
            except:
                pass
    
    # 播放变化设置
    def player_start_setting(self, mp3, num):
        
        self.lyr_num = 0
        self.lyrtime_num = 0
        
        if mp3 is None:
            self.player_stop_setting()
        else:
            # 改变音乐详情页的内容
            try:
                self.bt_play_change_song(mp3[0], mp3[1], mp3[4], num)
                self.player.setMedia(QMediaContent(QUrl.fromLocalFile(mp3[3])))
                self.horizontalSlider_speed.setValue(0)
                self.label_time_pre.setText("00:00")
                self.lyric_time_change_pre(mp3)
                self.player.play()
            
            except OSError as e:
                print(e)
    
    # 每一次停止都需要做的一些操作
    def bt_play_change_song(self, img_na, so_name, lyrics, num):
        global gl_So_na_lo
        try:
            # 播放列表红色字体突出
            bt_li = self.ing_mc.findChild(
                    QPushButton, "pushButton_ing_mc_so_name_{}".format(gl_So_na_lo)
            )
            bt_li.setStyleSheet(
                    'color: qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0 rgba(119, 180, 255, 255), '
                    'stop:0.857955 rgba(85, 230, 77, 255));text-align :left; '
            )
        except:
            pass
        self.pushButton_bottom_ini_logo.setStyleSheet(
                'QPushButton{border-radius:10px;background-color: rgb(227, 227, 227);border-image:url('
                'pachong/music/local/img/%s.jpg);}QPushButton:hover{opacity: 0.5;background-color: qlineargradient('
                'spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(247, 219, 221, 255), stop:0.965909 rgba(209, 230, '
                '255, 255));border-image: url(:/icon/icon/up.png);}' % img_na
        )
        # # 音乐界面的图片
        #
        # self.lable_page_music_decorate_img.setStyleSheet(
        #         'border-radius:125px;border: 18px solid  rgb(53, 53, 53); background-image: url('
        #         'pachong/music/local/img/{}.jpg);'.format(
        #                 img_na
        #         )
        # )
        
        # 歌曲信息的更新
        self.label_page_music_name.setText("{}".format(so_name))
        
        # self.label_bottom_ini_name.setText("{}".format(so_name))
        self.label_bottom_ini = img_na
        self.label_bottom_ini_name = so_name
        try:
            self.verticalLayout_13.removeWidget(self.scrollTextWindow)
        except:
            pass
        self.scrollTextWindow = ScrollTextWindow(img_na, so_name, 9, 20, self)
        self.verticalLayout_13.addWidget(self.scrollTextWindow)
        
        try:  # mp3
            # 实例化小部件的滚动字幕
            try:
                self.mp3.horizontalLayout_3.removeWidget(self.scrollTextWindow_mp3)
            except:
                pass
            self.scrollTextWindow_mp3 = ScrollTextWindow(img_na, so_name, 8, 12, self)
            self.mp3.horizontalLayout_3.addWidget(self.scrollTextWindow_mp3)
            
            self.mp3.mp3_information_logo_Bt.setStyleSheet(self.pushButton_bottom_ini_logo.styleSheet())
            self.mp3.mp3_information_name_L.setText("{}".format(so_name))
            self.mp3.mp3_information_inf_L.setText("{}".format(img_na))
        except:
            pass
        self.bt_change(num)
    
    # 播放时的按键变化
    def bt_change(self, num):
        global gl_Last_so_P
        self.pushButton_bottom_play.setObjectName('pause')
        self.pushButton_bottom_play.setIcon(QtGui.QIcon(':/icon/icon/pause.png'))  # 设置图标
        try:
            # mp3 的播放变化
            self.mp3.mp3_player_play_Bt.setObjectName('pause')
            self.mp3.mp3_player_play_Bt.setIcon(QtGui.QIcon(':/icon/icon/pause.png'))  # 设置图标
        except:
            pass
        try:
            bt_play_change = self.findChild(
                    QPushButton, "pushButton_song_list_bottom_play_{}_{}".format(gl_Last_so_P, str(num))
            )
            bt_play_change.setIcon(QtGui.QIcon(':/icon/icon/pause.png'))  # 设置图标
        except:  # 排行里歌单列表的播放图标，没加载就没有则不做处理
            try:
                bt_ranking_change = self.ra_list[gl_Last_so_P][0].findChild(
                        QPushButton, "ranking_list_Bottom_td_{}_play".format(
                                gl_Last_so_P + str(num + 1)
                        )
                )
                bt_ranking_change.setIcon(QtGui.QIcon(':/icon/icon/pause.png'))  # 设置图标
            except:
                pass
    
    # down下载按钮下载歌曲
    def bt_download_local(self):
        global gl_ing_url
        if gl_ing_url is None:
            print('当前无音乐，无法下载')
        else:
            
            self.mp3_download(gl_ing_url)

    """获取当前音乐的mp3连接,下载地址,名称"""
    def mp3_download(self, _ing_url):
        """获取当前音乐的mp3连接,下载地址,名称"""
        _mp3 = red_js('local', 'cache', _ing_url)
        down_load_mc(_ing_url,_mp3[3], self.file_path, _mp3[0])
        
    '''歌词动画组设置'''
    # 歌词随进度变化
    def lyric_time_change_pre(self, mp3):
        self.lyr = []
        for lyr in mp3[4]:
            self.lyr.append(int(lyr))
        # 时间列表排序
        self.lyr.sort()
        self.lyrime = QTimer()
        self.lyrime.start(10)
        # print(self.lyr_num, self.lyrtime_num)
        self.lyrime.timeout.connect(lambda: self.lyrime_label())  # 歌词高亮
        self.Lyrics_display(mp3[4])
    # 歌词变化动画策略
    def lyrime_label(self):
        # print(self.lyr_num, len(self.lyr))
        if self.lyr_num == len(self.lyr):
            self.lyrime.killTimer(0)
            self.lyr = []
            self.lyr_num = 0
            self.lyrtime_num = 0
        else:
            # print(self.lyrtime_num, self.lyr[self.lyr_num], self.lyr_num)
            if self.lyrtime_num > self.lyr[self.lyr_num]:
                try:
                    bt_lyrime_last = self.findChild(QLabel, "music_lyric_{}".format(self.lyr[self.lyr_num - 1]))
                    bt_lyrime_last.setStyleSheet('color:rgba(255, 255, 255, 255);')
                except:
                    pass
                bt_lyrime = self.findChild(QLabel, "music_lyric_{}".format(self.lyr[self.lyr_num]))
                bt_lyrime.setStyleSheet('font: 15pt "本墨字语";color: #dd3535;')
                
                # print(bt_lyrime.height())
                self.scrollArea_page_music_lyric.verticalScrollBar().setValue(80 * (self.lyr_num - 1))
                self.lyr_num += 1
        self.lyrtime_num += 10
    
    # 歌词label化
    def ui_Label_lyric(self, tim):
        label__music_lyric = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        label__music_lyric.setMinimumSize(QtCore.QSize(380, 80))
        label__music_lyric.setMaximumSize(QtCore.QSize(16777215, 80))
        font = QtGui.QFont()
        font.setFamily("本墨字语")
        font.setPointSize(13)
        font.setWeight(50)
        label__music_lyric.setFont(font)
        label__music_lyric.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignCenter)
        label__music_lyric.setStyleSheet("color:rgba(255, 255, 255, 255)")
        label__music_lyric.setObjectName("music_lyric_{}".format(tim))
        return label__music_lyric
    
    # 歌词展示
    def Lyrics_display(self, lyrics):
        if len(self.lyric) == 0:
            pass
        else:
            for ly in self.lyric:
                self.verticalLayout_16.removeWidget(ly)
            self.lyric.clear()
        
        for lyr in self.lyr:
            lyre = self.ui_Label_lyric(lyr)
            self.lyric.append(lyre)
            try:
                try:
                    # print(lyrics[lyr])
                    lyrs = lyrics[lyr].replace("\\", '')
                    # print(lyrs)
                except:
                    lyrs = lyrics[str(lyr)].replace("\\", '')
            except:
                try:
                    lyrs = lyrics[lyr]
                except:
                    lyrs = lyrics[str(lyr)]
            lyre.setText("{}".format(lyrs))  # 歌詞
            lyre.setWordWrap(True)  # 歌词显示自动换行
            self.verticalLayout_16.addWidget(lyre)
    
    '''歌词页面调用管理'''
    # 头像上拉单曲页面,(其他页面操作会自动跳转到头像组)
    def bt_page_music_alone(self):
        self.sign_so_detail_page()
        self.sWidget_middle(2)
        self.sWidget_bt(1)
    
    # 头像下拉退出单曲页面
    def bt_page_music_alone_out(self):
        self.sWidget_main(self.so_detail)
        self.sWidget_middle(0)
        self.sWidget_bt(0)
    
    '''主页面页面管理'''
    
    # 软件首页 self.index 返回是否在主页面
    # 0 不在则调用 self，so_detail(page值)为跳转页
    # 1 跳转到主页
    def bt_page_index(self):
        if self.index == 0:
            self.sWidget_main(self.so_detail)
            self.sWidget_middle(0)
            self.sWidget_bt(0)
            self.index = 1
        elif self.index == 1:
            self.sign_so_detail_page()
            self.sWidget_middle(1)
            self.sWidget_bt(0)
            self.index = 0
    
    # 退一步页面
    # self.sign_so_detail_page 为插旗返回self，so_detail(page值)
    # 调用self，so_detail(page值)跳转到上个页面
    # (留空还进则加入个记录函数，卡片，播放及其他记录页面项self.page_index_num)
    # 加入self.page_last来判断索引值，每次加入的时候索引值清零
    def bt_page_right(self):
        if len(self.page_index_num) == 0:
            pass
        else:
            if abs(self.page_last) == len(self.page_index_num) - 1:
                self.page_last = 0
            self.page_last -= 1
            self.sWidget_main(self.page_index_num[self.page_last])
            self.sWidget_bt(0)
            print(self.page_last, self.page_index_num[-2], self.page_index_num)
    
    # 下一步页面
    def bt_page_left(self):
        if self.page_last >= 0:
            pass
        else:
            if abs(self.page_last) == len(self.page_index_num) - 1:
                self.page_last = 0
            self.page_last += 1
            print(self.page_last)
            self.sWidget_main(self.page_index_num[self.page_last])
            self.sWidget_bt(0)
    
    '''推荐歌单'''
    
    # 音乐栏目(默认推荐)
    # 展示推荐页的卡片
    # 加载排行榜的信息
    def bt_page_music_index(self, alt_reco):
        na = 'reco'
        if len(self.mc_list[na]) == 0:
            mc_list = Ui_grid(na, alt_reco)
            self.mc_list[na].append(mc_list)
            self.verticalLayout_repo_page.addWidget(self.mc_list[na][0])
            for i in range(len(alt_reco)):
                self.grid_click_connect(na, i, alt_reco[i])
        # 卡片刷新之后再刷新排行榜
        name_rank = ['soar', 'hotsong', 'newsong']
        for nai in name_rank:
            # print(len(self.ra_list[nai]))
            if len(self.ra_list[nai]) == 0:
                # 加载排行
                self.ranking_List(nai)
                sleep(0.01)
        self.sWidget_reo_mc(0)
        self.sWidget_main(2)
        self.sWidget_bt(0)
    
    # 推荐歌单
    def bt_page_music_reo(self, alt_reco):
        self.pushButton_tab_reco_music_reco.setEnabled(False)
        self.pushButton_tab_reco_music_hot.setEnabled(True)
        self.pushButton_tab_index_music_collection.setEnabled(True)
        self.pushButton_tab_index_music_rise.setEnabled(True)
        na = 'reco'
        if len(self.mc_list[na]) == 0:
            mc_list = Ui_grid(na, alt_reco)
            self.mc_list[na].append(mc_list)
            self.verticalLayout_repo_page.addWidget(self.mc_list[na][0])
            for i in range(len(alt_reco)):
                self.grid_click_connect(na, i, alt_reco[i])
        self.sWidget_reo_mc(0)
    
    # 最热歌单
    def bt_page_music_hot(self, alt_hot):
        self.pushButton_tab_reco_music_reco.setEnabled(True)
        self.pushButton_tab_reco_music_hot.setEnabled(False)
        self.pushButton_tab_index_music_collection.setEnabled(True)
        self.pushButton_tab_index_music_rise.setEnabled(True)
        na = 'hot'
        if len(self.mc_list[na]) == 0:
            mc_list = Ui_grid(na, alt_hot)
            self.mc_list[na].append(mc_list)
            self.verticalLayout_mc_reco_hot.addWidget(self.mc_list[na][0])
            for i in range(len(alt_hot)):
                self.grid_click_connect(na, i, alt_hot[i])
        self.sWidget_reo_mc(1)
    
    # 收藏歌单
    def bt_page_music_collection(self, alt_collection):
        self.pushButton_tab_reco_music_reco.setEnabled(True)
        self.pushButton_tab_reco_music_hot.setEnabled(True)
        self.pushButton_tab_index_music_collection.setEnabled(False)
        self.pushButton_tab_index_music_rise.setEnabled(True)
        na = 'collection'
        if len(self.mc_list[na]) == 0:
            mc_list = Ui_grid(na, alt_collection)
            self.mc_list[na].append(mc_list)
            self.verticalLayout_mc_reco_collection.addWidget(self.mc_list[na][0])
            for i in range(len(alt_collection)):
                self.grid_click_connect(na, i, alt_collection[i])
        self.sWidget_reo_mc(2)
    
    # 飙升歌单
    def bt_page_music_rise(self, alt_rise):
        self.pushButton_tab_reco_music_reco.setEnabled(True)
        self.pushButton_tab_reco_music_hot.setEnabled(True)
        self.pushButton_tab_index_music_collection.setEnabled(True)
        self.pushButton_tab_index_music_rise.setEnabled(False)
        na = 'rise'
        if len(self.mc_list[na]) == 0:
            mc_list = Ui_grid(na, alt_rise)
            self.mc_list[na].append(mc_list)
            self.verticalLayout_mc_reco_rise.addWidget(self.mc_list[na][0])
            for i in range(len(alt_rise)):
                self.grid_click_connect(na, i, alt_rise[i])
        self.sWidget_reo_mc(3)
    
    '''排行榜'''
    
    # 排行榜
    def ranking_List(self, na):
        fol_na = r'kg\ranking_page'
        self.ranking_js_Th(fol_na, na, 'alt')
        if na == 'soar':
            self.open_all_Bt.clicked.connect(lambda: self.ranking_list_show(na))
        if na == 'hotsong':
            self.open_all_Bt_2.clicked.connect(lambda: self.ranking_list_show(na))
        if na == 'newsong':
            self.open_all_Bt_3.clicked.connect(lambda: self.ranking_list_show(na))
    
    # 排行榜读取数据槽函数
    def ranking_js_Th(self, fol_na, fi_na, group):
        self.soar = re_js_thread()
        if fi_na == 'soar':
            self.soar.sinout.connect(self.soar_list)
        elif fi_na == 'hotsong':
            self.soar.sinout.connect(self.hot_song)
        elif fi_na == 'newsong':
            self.soar.sinout.connect(self.new_song)
        self.soar.set_param(fol_na, fi_na, group)
        self.soar.start()
    
    # 飙升榜列表页
    def soar_list(self, alt):
        self.label_tab_index_music_m_Ranking_up_na_1.setText(alt[0])
        self.label_tab_index_music_m_Ranking_up_na_2.setText(alt[1])
        self.label_tab_index_music_m_Ranking_up_na_3.setText(alt[2])
        self.label_tab_index_music_m_Ranking_up_na_4.setText(alt[3])
        self.label_tab_index_music_m_Ranking_up_na_5.setText(alt[4])
        na = 'soar'
        ra_li = Ui_ra_list(na, alt)
        self.ra_list[na].append(ra_li)
    
    # 热门榜列表页
    def hot_song(self, alt):
        self.label_tab_index_music_m_Ranking_up_na_6.setText(alt[0])
        self.label_tab_index_music_m_Ranking_up_na_7.setText(alt[1])
        self.label_tab_index_music_m_Ranking_up_na_8.setText(alt[2])
        self.label_tab_index_music_m_Ranking_up_na_9.setText(alt[3])
        self.label_tab_index_music_m_Ranking_up_na_10.setText(alt[4])
        na = 'hotsong'
        ra_li = Ui_ra_list(na, alt)
        self.ra_list[na].append(ra_li)
    
    # 新歌榜列表页
    def new_song(self, alt):
        self.label_tab_index_music_m_Ranking_up_na_11.setText(alt[0])
        self.label_tab_index_music_m_Ranking_up_na_12.setText(alt[1])
        self.label_tab_index_music_m_Ranking_up_na_13.setText(alt[2])
        self.label_tab_index_music_m_Ranking_up_na_14.setText(alt[3])
        self.label_tab_index_music_m_Ranking_up_na_15.setText(alt[4])
        na = 'newsong'
        ra_li = Ui_ra_list(na, alt)
        self.ra_list[na].append(ra_li)
    
    # 排行榜歌单列表
    def ranking_list_show(self, na):
        global gl_Last_so_P
        try:
            if gl_Last_so_P.split('_')[-1].isdigit():
                self.so_list_P[gl_Last_so_P][0].close()
            else:
                self.ra_list[gl_Last_so_P][0].close()
        except:
            pass
        gl_Last_so_P = na
        self.ra_list[na][0].show()
        # print(self.ra_list[na][0])
        self.ranking_list_SA_LY.addWidget(self.ra_list[na][0])
        self.sWidget_main(5)
        # 绑定排行榜播放按钮函数
        self.set_ranking_thread(na)
        self.bt_ranking_list_all_play(gl_Last_so_P)
    
    # 获取歌链接的线程
    def set_ranking_thread(self, na):
        self.re_ranking = re_js_thread()
        self.re_ranking.sinout.connect(self.bt_ranking_list)
        self.re_ranking.set_param(r'kg\ranking_page', na, 'href')
        self.re_ranking.start()
    
    # 排行榜歌单
    def bt_ranking_list(self, so_src):
        for i in range(len(so_src)):
            self.bt_ranking_player(i, so_src[i])  # 拿到对应的22个排行榜音乐的链接连接槽
    
    # 排行榜歌单播放
    def bt_ranking_player(self, num, so_src):
        global gl_Last_so_P
        
        bt_ranking_play = self.ra_list[gl_Last_so_P][0].findChild(
                QPushButton, "ranking_list_Bottom_td_{}_play".format(
                        gl_Last_so_P + str(num + 1)
                )
        )
        bt_ranking_play.disconnect()
        bt_ranking_play.clicked.connect(lambda: self.bt_player_connect(num, so_src))
    
    # 排行榜列表的全部音乐播放
    def bt_ranking_list_all_play(self, na):
        global nu
        nu = 0
        bt_ranking_list_play = self.ra_list[na][0].findChild(
                QPushButton, "ranking_list_Bottom_td_0_Bt_play_{}".format(na)
        )
        bt_ranking_list_play.clicked.connect(lambda: self.all_ranking_thread(na))
    
    # 排行榜歌单choice对应全部播放列表
    def rank_choice(self, cl_p):
        n = 0
        while True:
            bt_radio = self.ra_list[cl_p][0].findChild(
                    QRadioButton, "ranking_list_Bottom_td_{}_choice".format(cl_p + str(n + 1))
            )
            # print(bt_radio)
            if not bt_radio:
                # print(n)
                return n
            n += 1
    
    # 排行榜歌单全部播放线程
    def all_ranking_thread(self, cl_p):
        no = []
        ran = self.rank_choice(cl_p)
        for i in range(ran):
            bt_radio = self.ra_list[cl_p][0].findChild(
                    QRadioButton, "ranking_list_Bottom_td_{}_choice".format(cl_p + str(i + 1))
            )
            if bt_radio.isChecked():
                no.append(i)
        print(no)
        self.all_li = add_ranking_thread()
        self.all_li.toout.connect(self.all_so_ing_list)
        self.all_li.set_param(cl_p)
        self.all_li.start()
    
    def ing_change_to_ed(self):
        self.mc_manage_loading_Bt.setStyleSheet('')
        self.mc_manage_loaded_Bt.setStyleSheet(
                "color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,stop:0.369318 rgba(136, 147, 255, 255), stop:1 rgba(137, 255, 151,255)); "
                "border: 1px solid qlineargradient(spread: pad, x1: 1, y1: 1, x2: 0, y2: 0, stop: 0 rgba(161, 174, 255, 255), stop: 0.863636 rgba(74, 129, 230, 255));"
                "border-radius: 11px;"
        )
    
    def ed_change_to_ing(self):
        self.mc_manage_loaded_Bt.setStyleSheet('')
        self.mc_manage_loading_Bt.setStyleSheet(
                "color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,stop:0.369318 rgba(136, 147, 255, 255), stop:1 rgba(137, 255, 151,255)); "
                "border: 1px solid qlineargradient(spread: pad, x1: 1, y1: 1, x2: 0, y2: 0, stop: 0 rgba(161, 174, 255, 255), stop: 0.863636 rgba(74, 129, 230, 255));"
                "border-radius: 11px;"
        )
    
    # 本地音乐
    def bt_page_music_local(self):
        self.sWidget_main(3)
        self.sWidget_bt(0)
        self.sWidget_local(0)
        self.sign_so_detail_page()
        self.ing_change_to_ed()
    
    # 正在下载界面
    def mc_Mg_loading_Bt(self):
        self.ed_change_to_ing()
        self.sWidget_local(1)
    # 已完成下载界面
    def mc_Mg_loaded_Bt(self):
        self.ing_change_to_ed()
        self.sWidget_local(0)
    # 正在下载单曲选择目录
    def mc_pathEd_Bt(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹", self.p_path)  # 起始路径
        print(directory)
        self.path_La.setText(directory)
        self.to_ini('mc_pathEd_for', 'p_path', directory)
    # 已经下载单曲选择目录
    def mc_pathIng_Bt(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹", self.ping_path)  # 起始路径
        self.path_LA.setText(directory)
        self.to_ini('mc_pathIng_for', 'p_path', directory)
    # 本地歌曲
    def file_Path_Bt(self):
        try:
            for local in self.mc_local_list:
                self.mc_local_list_VL.removeWidget(local)
            self.mc_local_list.clear()
        except:
            pass
        directory = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹", self.file_path)  # 起始路径
        self.file_Path.setText(directory)
        self.to_ini('file_path', 'p_path', directory)
        file_names = file_fol(directory)
        print(file_names)
        x = 1
        for so_name in file_names['mp3']:
            num = x
            so_ti = '00:00'
            local_list = Ui_local_mc_list(num, so_name, so_ti)
            self.mc_local_list_VL.addWidget(local_list)
            self.mc_local_list.append(local_list)
            x += 1
        self.howManySong.setText('本地共有{}首歌曲'.format(len(file_names['mp3'])))
        
    
    # 最近浏览
    def bt_page_music_localbrowse(self):
        self.sWidget_main(4)
        self.sWidget_bt(0)
        self.sign_so_detail_page()
    
    # 绑定卡片事件按钮
    def grid_click_connect(self, na, num, alt_na):
        bt_solist = self.findChild(QPushButton, "pushButton_list_{}_{}".format(na, str(num)))
        bt_solist.disconnect()
        bt_solist.clicked.connect(lambda: self.bt_songlist_page(na, num, alt_na))  # 连接歌单列表页
    
    # 没有则线程创建歌单列表
    def bt_songlist_page(self, na, num, alt_na):
        # 详情页返回插眼
        self.sign_so_detail_page()
        # 获取列表详细信息线程
        self.load_so = set_songlist_page_Th()
        self.load_so.toout.connect(self.load_so_list)
        self.load_so.set_param(r'kg\reco_page', 'mc_{}_inf'.format(na), na, num, alt_na)
        self.load_so.start()
    
    # 加载so_list详情页,模板生成
    def load_so_list(self, grid_na, im_path, alt_na, inf_iny, so_name):
        if self.so_list_P[grid_na]:
            # print(self.so_list_P)
            print('模板中，不用生成')
        else:
            grid_li = ui_grid_li(grid_na, im_path, alt_na, inf_iny, so_name)
            # print(grid_li)
            self.so_list_P[grid_na].append(grid_li)
        self.bt_all_li_play(grid_na)
        # 绑定播放列表播放按钮线程
        self.open_songlist(grid_na)
        self.re_js = re_js_thread()
        self.re_js.sinout.connect(self.bt_pl_solt)
        self.re_js.set_param(r'kg\reco_page', 'mc_{}_inf'.format(grid_na.split('_')[0]), 'song')
        self.re_js.start()
    
    def bt_all_li_play(self, grid_na):
        # 绑定全部列表的play按钮
        bt_song_list_play = self.so_list_P[grid_na][0].findChild(
                QPushButton,
                "pushButton_song_list_top_play_{}".format(grid_na)
        )
        bt_song_list_play.disconnect()
        bt_song_list_play.clicked.connect(lambda: self.all_li_play_thread(grid_na))
    
    # 显示歌单列表页
    def open_songlist(self, grid_na):
        global gl_Last_so_P
        global gl_Page_and_num
        print('播放的单曲的定位' + '=' + str(gl_Page_and_num))
        print('上一次打开列表的页面' + '=' + str(gl_Last_so_P))
        try:
            if gl_Last_so_P.split('_')[-1].isdigit():
                self.so_list_P[gl_Last_so_P][0].close()
            else:
                self.ra_list[gl_Last_so_P][0].close()
        except:
            pass
        # 更新gl_Last_so_P为现在的歌单页
        gl_Last_so_P = grid_na
        print('现在的列表页：' + str(gl_Last_so_P))
        self.so_list_P[grid_na][0].show()
        self.verticalLayout_mc_reco_reco_inf.addWidget(self.so_list_P[grid_na][0])
        self.sWidget_main(6)
    
    # 绑定播放按钮的槽函数
    def bt_pl_solt(self, song):
        global gl_Last_so_P
        num = gl_Last_so_P.split('_')[-1]
        so_src = song[int(num)]['so_src']
        for i in range(len(so_src)):
            self.bt_player(i, so_src[i])
    
    def bt_player(self, num, so_url):
        global gl_Last_so_P
        bt_play = self.so_list_P[gl_Last_so_P][0].findChild(
                QPushButton, "pushButton_song_list_bottom_play_{}_{}".format(
                        gl_Last_so_P, str(num)
                )
        )
        bt_play.disconnect()
        bt_play.clicked.connect(lambda: self._bt_player_connect(num, so_url))
        # 单曲下载
        bt_download = self.so_list_P[gl_Last_so_P][0].findChild(
                QPushButton, "pushButton_song_list_bottom_download_{}_{}".format(
                        gl_Last_so_P, str(num)
                )
        )
        bt_download.disconnect()
        try:
            # 重写已下载的图标，并不可点击
            with open(r'pachong\music\local\dload_Ed.json', encoding='utf-8') as r:
                dload_url = json.load(r)
            r.close()
            if so_url in dload_url:
                bt_download.setIcon(QtGui.QIcon(':/icon/icon/dload_ok.png'))  # 设置图标
                bt_download.setEnabled(False)
            else:
                bt_download.clicked.connect(lambda: self.bt_dload_thread(so_url, num))
        except:
            bt_download.clicked.connect(lambda: self.bt_dload_thread(so_url, num))
            
    def bt_dload_thread(self, so_url, num):
        self.dload_mp3 = dload_mp3_thread()
        self.dload_mp3.mp3_out.connect(self._bt_download_connect)
        self.dload_mp3.set_param(so_url,num)
        self.dload_mp3.start()
    # 下载单曲音乐
    def _bt_download_connect(self, so_url, mp3, num):
        global gl_Last_so_P
        down_load_mc(so_url, mp3[3], self.file_path, mp3[0])
        # 单曲下载
        bt_download = self.so_list_P[gl_Last_so_P][0].findChild(
                QPushButton, "pushButton_song_list_bottom_download_{}_{}".format(
                        gl_Last_so_P, str(num)
                )
        )
        # 重写已下载的图标，并不可点击
        bt_download.setIcon(QtGui.QIcon(':/icon/icon/dload_ok.png'))  # 设置图标
        bt_download.setEnabled(False)
    
        
    # 单点播放音乐
    def _bt_player_connect(self, num, so_url):
        global nu
        global gl_All_list_play
        nu = 0
        gl_All_list_play = []
        # 换音乐，先停止设置
        # print(gl_All_list_play)
        self.player_stop_setting()
        self.bt_player_connect(num, so_url)  # 线程加载缓存音乐
    
    def bt_player_connect(self, num, so_src):
        global gl_Page_and_num
        global gl_ing_url
        global gl_Last_so_P
        print(gl_Last_so_P, str(num) + '这两个')
        gl_ing_url = so_src
        print('gl_ing_url' + '=' + gl_ing_url)
        if len(gl_Page_and_num) == 0:  # 播放的音乐标签
            self.bt_player_thread(num)  # 线程加载缓存音乐
        else:
            if gl_Last_so_P == gl_Page_and_num[0] and num == gl_Page_and_num[1]:
                if len(gl_Page_and_num) == 3:
                    print('play')
                    self.bt_change(num)
                    self.player.play()
                    gl_Page_and_num = [gl_Page_and_num[0], num]
                elif len(gl_Page_and_num) == 2:
                    self.bt_pause()
                    print('pause')
            else:
                # 换音乐，先停止设置
                self.player_stop_setting()
                self.bt_player_thread(num)  # 线程加载缓存音乐
    
    def bt_player_thread(self, num):
        self.set_mp3 = get_mp3_thread()
        self.set_mp3.sinout.connect(self.player_start_setting)
        self.set_mp3.set_param(num)
        self.set_mp3.start()
    
    def reco_choice(self, grid_na):
        n = 0
        while True:
            bt_radio = self.so_list_P[grid_na][0].findChild(
                    QRadioButton, "radioButton_song_list_bottom_choice_{}_{}".format(grid_na, n)
            )
            
            # print(bt_radio)
            if not bt_radio:
                # print(n)
                return n
            n += 1
    
    def all_li_play_thread(self, grid_na):
        no = []
        res = self.reco_choice(grid_na)
        for i in range(res):
            bt_radio = self.so_list_P[grid_na][0].findChild(
                    QRadioButton,
                    "radioButton_song_list_bottom_choice_{}_{}".format(grid_na, i)
            )
            if bt_radio.isChecked():
                no.append(i)
        # print(no)
        self.all_li = add_list_thread()
        self.all_li.toout.connect(self.all_so_ing_list)
        self.all_li.set_param(grid_na, no)
        self.all_li.start()
    
    def all_so_ing_list(self, all_li):
        global nu
        global gl_All_list_play
        nu = 0
        gl_All_list_play = all_li
        global gl_Last_so_P
        global gl_ing_url
        gl_Last_so_P = gl_All_list_play[nu][0]
        gl_ing_url = gl_All_list_play[nu][2]
        self.player_stop_setting()
        self.bt_player_thread(gl_All_list_play[nu][1])  # 线程加载缓存音乐
        # self.bt_player_connect(gl_All_list_play[nu][1], gl_All_list_play[nu][2])
    
    # 按键播放
    
    def bt_bottom_play(self):
        global gl_Page_and_num
        global gl_ing_url
        global gl_Last_so_P
        if len(gl_Page_and_num) == 0:  # 没有音乐在播放
            # 这边自动播放上次的位置
            last_so = self.get_ini('so_save', 'last_so')
            la = last_so.split('|')
            gl_ing_url = la[2]
            gl_Last_so_P = la[0]
            self.bt_player_thread(la[1])
            '''留空'''
        elif len(gl_Page_and_num) == 3:  # 有暂停的歌曲
            # print(gl_Page_and_num)
            self.bt_change(gl_Page_and_num[1])
            self.player.play()
            gl_Page_and_num = [gl_Page_and_num[0], gl_Page_and_num[1]]
        elif len(gl_Page_and_num) == 2:  # 有播放的歌曲
            self.bt_pause()
            print('bt_pause')
    
    # 按键暂停
    def bt_pause(self):
        global gl_Page_and_num
        self.player.pause()
        self.bt_pause_change_song(gl_Page_and_num[0], gl_Page_and_num[1])
        gl_Page_and_num = [gl_Page_and_num[0], gl_Page_and_num[1], 'pause']
    
    # 计时时间到了做处理
    def timeout_process(self):
        if self.pushButton_bottom_play.objectName() == "pause":
            time_value = self.horizontalSlider_speed.value()
            self.horizontalSlider_speed.setValue(time_value + 1)
            self.label_time_pre.setText(
                    str((time_value + 1) // 60).zfill(2) + ':' + str((time_value + 1) % 60).zfill(2)
            )
            
            try:
                self.mp3.mp3_time_pre_L.setText(self.label_time_pre.text())
            except:
                pass
            time_long = self.player.duration()  # 获取到实际这首歌的播放长度
            if time_long == 0:
                self.next_music()
            else:
                if self.label_time_pre.text() == "00:01":
                    self.horizontalSlider_speed.setRange(0, int(time_long / 1000) + 1)  # 设置进度条范围
                    self.label_time_next.setText(
                            str(int(time_long / 1000) // 60).zfill(2) + ':' + str(int(time_long / 1000) % 60).zfill(2)
                    )  # 设置音频长度的显示
                    try:
                        self.mp3.label_time_next_mp3.setText(self.label_time_next.text())  # 设置音频长度的显示
                    except:
                        pass
                    so_ti_lo = str(int(time_long / 1000) // 60).zfill(2) + ':' + str(int(time_long / 1000) % 60).zfill(
                            2
                    )
                    self.sa_ing_li(so_ti_lo)
                elif self.label_time_pre.text() == self.label_time_next.text():
                    self.next_music()
    
    def sa_ing_li(self, so_ti_lo):
        da_url = defaultdict(list)
        global gl_ing_url
        global gl_Page_and_num
        fol_na = 'local'
        fi_na = 'sa_ing_li'
        da_url[gl_ing_url].append(gl_Page_and_num[0])
        da_url[gl_ing_url].append(int(gl_Page_and_num[1]))
        da_url[gl_ing_url].append(so_ti_lo)
        
        try:
            obt = obt_js(fol_na, fi_na)
            add_js_data(fol_na, fi_na, obt, da_url)
        except:
            wr_js(fol_na, fi_na, da_url)
        try:
            self.ing_mc.updata_mc_Menu(gl_ing_url, so_ti_lo)
        except:
            # 清楚掉了
            pass
    
    # 调节播放进度
    def music_time_adjust(self):
        try:
            bt_lyrime_last = self.findChild(QLabel, "music_lyric_{}".format(self.lyr[self.lyr_num - 1]))
            bt_lyrime_last.setStyleSheet('color:rgba(255, 255, 255, 255);')
        except:
            pass
        self.player.pause()
        self.player.setPosition(self.horizontalSlider_speed.value() * 1000)
        
        # print(self.lyrtime_num)
        n = 0
        # 定位到歌词进度
        for lr in self.lyr:
            if lr >= self.horizontalSlider_speed.value() * 1000:
                self.lyr_num = n
                # print(lr)
                return
            n += 1
    
    # 调节进度完成
    def music_time_adjust_over(self):
        self.player.play()
        self.lyrtime_num = self.horizontalSlider_speed.value() * 1000
    
    # 调节音量
    def volume_adjust(self):
        try:
            self.player.setVolume(100 - (self.horizontalSlider.value()))
            self.label_volume_adjust.setText("{}%".format(100 - (self.horizontalSlider.value())))
            if self.horizontalSlider.value() == 100:
                self.pushButton_bottom_volume.setIcon(QtGui.QIcon(":/icon/icon/volume_closs.png"))
            elif 50 < self.horizontalSlider.value() < 99:
                self.pushButton_bottom_volume.setIcon(QtGui.QIcon(":/icon/icon/volume_big.png"))
            elif 0 < self.horizontalSlider.value() < 49:
                self.pushButton_bottom_volume.setIcon(QtGui.QIcon(":/icon/icon/volume.png"))
        except:
            print('还没有播放音乐')
    
    # 下一首线程
    def next_music_thread(self):
        next_music = threading.Thread(target=self.next_music)
        next_music.start()
    
    # 上一首线程
    def last_music_thread(self):
        last_music = threading.Thread(target=self.last_music)
        last_music.start()
    
    def next_music(self):
        # self.lock.acquire()
        global gl_So_na_lo
        try:
            li = self.ing_mc.findChild(
                    QPushButton, "pushButton_ing_mc_so_name_{}".format(gl_So_na_lo)
            )
            li.setStyleSheet("color :rgb(0,0,0);text-align :left;")
        except:
            pass
        global gl_ing_url
        global nu
        global gl_All_list_play
        if len(gl_All_list_play) != 0:
            nu += 1
            if nu == len(gl_All_list_play):
                nu = 0
                gl_All_list_play = []
            else:
                self.bt_player_connect(gl_All_list_play[nu][1], gl_All_list_play[nu][2])
        
        else:
            fol_na = 'local'
            fi_na = 'sa_ing_li'
            if self.pushButton_bottom_playbar_pattern.objectName() == 'loop':  # 循环播放
                try:
                    in_so = self.so_src_list.index(gl_ing_url)
                    # print(in_so.index(gl_ing_url))
                    obt = obt_js(fol_na, fi_na)
                    if in_so == len(self.so_src_list) - 1:
                        in_so = -1
                    else:
                        pass
                    no = in_so + 1
                    src = self.so_src_list[no]
                    num = obt[src][1]
                    gl_ing_url = src
                    self.player_stop_setting()
                    self.bt_player_thread(num)  # 线程加载缓存音乐
                except:
                    self.player_stop_setting()
            elif self.pushButton_bottom_playbar_pattern.objectName() == 'loop_along':  # 单曲循环
                global gl_Page_and_num
                self.player_stop_setting()
                self.bt_player_thread(gl_Page_and_num[1])  # 线程加载缓存音乐
            elif self.pushButton_bottom_playbar_pattern.objectName() == 'random':  # 随机循环
                try:
                    obt = obt_js(fol_na, fi_na)
                    x = random.randint(0, len(obt) - 1)
                    src = self.so_src_list[x]
                    num = obt[src][1]
                    gl_ing_url = src
                    self.player_stop_setting()
                    self.bt_player_thread(num)  # 线程加载缓存音乐
                except:
                    self.player_stop_setting()
        
        # self.lock.release()
    
    def last_music(self):
        self.lock.acquire()
        self.player_stop_setting()
        global gl_ing_url
        
        fol_na = 'local'
        fi_na = 'sa_ing_li'
        try:
            in_so = self.so_src_list.index(gl_ing_url)
            obt = obt_js(fol_na, fi_na)
            if in_so == 0:
                in_so = len(self.so_src_list)
            else:
                pass
            no = in_so - 1
            src = self.so_src_list[no]
            num = obt[src][1]
            gl_ing_url = src
            self.bt_player_thread(num)  # 线程加载缓存音乐
        except:
            self.player_stop_setting()
        self.lock.release()
    
    # 模式按钮响应
    def bt_playbar_pattern(self):
        
        if self.pushButton_bottom_playbar_pattern.objectName() == 'loop':  # 循环播放
            self.pushButton_bottom_playbar_pattern.setIcon(QtGui.QIcon(':/icon/icon/loop_along.png'))  # 设置图标
            self.pushButton_bottom_playbar_pattern.setObjectName('loop_along')  # 循环播放
            self.to_ini('pattern', 'pattern', 'loop_along')
            try:
                self.mp3.mp3_player_pattern_Bt.setIcon(QtGui.QIcon(':/icon/icon/loop_along.png'))  # 设置图标
                self.mp3.mp3_player_pattern_Bt.setObjectName('loop_along')  # 循环播放
            except:
                pass
        elif self.pushButton_bottom_playbar_pattern.objectName() == 'loop_along':  # 单曲循环
            self.pushButton_bottom_playbar_pattern.setIcon(QtGui.QIcon(':/icon/icon/random.png'))  # 设置图标
            self.pushButton_bottom_playbar_pattern.setObjectName('random')  # 单曲循环
            self.to_ini('pattern', 'pattern', 'random')
            try:
                self.mp3.mp3_player_pattern_Bt.setIcon(QtGui.QIcon(':/icon/icon/random.png'))  # 设置图标
                self.mp3.mp3_player_pattern_Bt.setObjectName('random')  # 单曲循环
            except:
                pass
        
        elif self.pushButton_bottom_playbar_pattern.objectName() == 'random':  # 随机循环
            self.pushButton_bottom_playbar_pattern.setIcon(QtGui.QIcon(':/icon/icon/loop.png'))  # 设置图标
            self.pushButton_bottom_playbar_pattern.setObjectName('loop')  # 随机循环
            self.to_ini('pattern', 'pattern', 'loop')
            try:
                self.mp3.mp3_player_pattern_Bt.setIcon(QtGui.QIcon(':/icon/icon/loop.png'))  # 设置图标
                self.mp3.mp3_player_pattern_Bt.setObjectName('loop')  # 随机循环
            except:
                pass
    
    # 正在播放的歌单
    def bt_mc_menu(self):
        if self.so_serial == 0:
            self.ing_mc.show()
            self.so_serial = 1
        else:
            self.ing_mc.close()
            self.so_serial = 0
        self.ing_play_thread()
    
    def ing_play_thread(self):
        self.re_ing = re_so_ing_thread()
        self.re_ing.sinout.connect(self.ing_play)
        self.re_ing.start()
    
    # 线程返回信号值循环处理
    def ing_play(self, lsr, lo_cl, lo_num, lo_na):
        i = 0
        for l in lsr:
            self.bt_ing_play(l, lo_cl[i], lo_num[i], lo_na[i][0])
            i += 1
    
    # 信号绑定播放列表按钮槽函数
    def bt_ing_play(self, so_scr, so_cl, so_num, so_na):
        bt_ = self.ing_mc.findChild(QPushButton, "pushButton_ing_mc_so_name_{}".format(so_na))
        if bt_:
            bt_.clicked.connect(lambda: self.bt_ing_and(so_scr, so_cl, so_num, so_na))
    
    # 播放列表播放槽函数
    def bt_ing_and(self, so_scr, so_cl, so_num, so_na):
        global gl_ing_url
        global gl_Last_so_P
        global gl_So_na_lo
        self.player_stop_setting()
        gl_So_na_lo = so_na
        gl_Last_so_P = so_cl
        gl_ing_url = so_scr
        self.bt_player_thread(so_num)
    
    def refresh_index(self):
        ix = self.get_sWidget_reco()
        if_na = ['reco', 'hot', 'collection', 'rise']
        in_na = if_na[ix]
        self.refresh = refresh_thread()
        if ix == 0:
            self.verticalLayout_repo_page.removeWidget(self.mc_list[in_na][0])
            del self.mc_list[in_na]
            self.refresh.toout.connect(self.set_reco_thread)
        if ix == 1:
            self.verticalLayout_repo_page.removeWidget(self.mc_list[in_na][0])
            del self.mc_list[in_na]
            self.refresh.toout.connect(self.set_hot_thread)
        if ix == 2:
            self.verticalLayout_repo_page.removeWidget(self.mc_list[in_na][0])
            del self.mc_list[in_na]
            self.refresh.toout.connect(self.set_collection_thread)
        if ix == 3:
            self.verticalLayout_repo_page.removeWidget(self.mc_list[in_na][0])
            del self.mc_list[in_na]
            self.refresh.toout.connect(self.set_rise_thread)
        self.refresh.set_param(in_na)
        self.refresh.start()


class get_mp3_thread(QThread):
    sinout = pyqtSignal(list, int)  # 自定义信号，执行run()函数时，从相关线程发射此信号
    
    def __init__(self):
        super(get_mp3_thread, self).__init__()
        self.mp3 = None
        self.num = None
    
    def set_param(self, num):
        self.num = num
    
    def run(self):
        global gl_Page_and_num
        global gl_ing_url
        global gl_Last_so_P
        global gl_So_na_lo
        qmut_3.lock()
        
        try:
            cache = red_cache()
            if len(cache[gl_ing_url]) != 0:
                self.mp3 = cache[gl_ing_url]
        except:
            self.mp3 = get_mp3_js(gl_ing_url)
        
        if self.mp3 is True:
            print('此歌曲当前无法播放,点击下面链接手动解锁滑块')
            print(
                    'https://www.kugou.com/mixsong/j3pry11.html#hash=6F64D67C0E499C0636A85807EC0F0EC5&album_id=965221&album_audio_id=32086078'
            )
            self.mp3 = None
            self.num = None
        else:
            try:
                gl_Page_and_num = [gl_Last_so_P, self.num]
                gl_So_na_lo = self.mp3[0]
                # print(self.mp3[3], gl_ing_url)
                staging = gl_Last_so_P + '|' + str(self.num) + '|' + gl_ing_url
                to_ini('so_save', 'last_so', str(staging))
                # 加载音乐图片,缓存有则跳过，无则下载
                fi_na = file_fol('pachong/music/local/img')
                if self.mp3[0] in fi_na['jpg']:
                    print('已有图片')
                else:
                    dload_image(self.mp3[2], 'pachong/music/local/img', self.mp3[0] + '.jpg')
            except:
                pass
        self.sinout.emit(self.mp3, self.num)
        qmut_3.unlock()
