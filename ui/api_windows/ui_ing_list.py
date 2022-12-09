# -*- coding: UTF-8 -*-
from collections import defaultdict
from PyQt5 import sip
from PyQt5.QtCore import pyqtSignal, Qt, QTimer
from PyQt5.QtWidgets import QWidget
from pachong.music.kg_mc import red_cache, obt_js, wr_js
from thread_mc.thread_mc import re_so_ing_thread
from ui.template.ing_mc import Ui_ing_mc
from ui.template.li import Ui_li

# 播放列表子窗口




class ui_ing_mc(QWidget, Ui_ing_mc):
    ing_clean = pyqtSignal()
    src_list_sign = pyqtSignal(list)
    
    
    def __init__(self):
        super(ui_ing_mc, self).__init__()
        self.li = defaultdict(list)
        
        self.so_src_list = []
        self.setupUi(self)
        # 读取正在播放的列表url线程
        self.re_ing_thread()
        # 初始化
        self.setAttribute(Qt.WA_TranslucentBackground)  # 窗体背景透明
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)  # 窗口置顶，无边框，在任务栏不显示图标
        self.move(1157, 248)
        self.m_flag = False
        self.pushButton_ing_mc_top_clear.clicked.connect(lambda: self.ing_clear())  # 清理列表get_so_src_list
        

    
    # 读取正在播放的列表url线程
    def re_ing_thread(self):
        """
        :return: mp3_lo, lsr, lo_ti
        :rtype: list，list，list
        """
        self.re_ing = re_so_ing_thread()
        self.re_ing.toout.connect(self.creat_mc_Menu)  # 创建正在播放的歌单
        self.re_ing.start()
        
        # 更新数目
    
    def updata_num(self):
        try:
            num = len(self.li)
            self.label_ing_mc_top_collection_num.setText('总{}首'.format(str(num)))
            self.get_so_src_list()
        except:
            pass
    
    # 创建正在播放的歌单
    def creat_mc_Menu(self, mp3_lo, lsr, lo_ti):
        """
        :param mp3_lo: 单曲的详细信息
        :type mp3_lo:  list
        :param lsr: 歌单里所有url
        :type lsr: list
        :param lo_ti:单曲时长
        :type lo_ti: list
        :return:
        :rtype:
        """
        
        self.so_src_list = lsr
        i = 0
        for mp3_li in mp3_lo:
            ing_list = Ui_li(mp3_li[0], lo_ti[i])
            self.verticalLayout_ing_mc_so.addWidget(ing_list)
            self.li[lsr[i]].append(ing_list)
            i += 1
        # 更新数目
        self.updata_num()
    
    # 更新正在播放的列表
    def updata_mc_Menu(self, ing_url, so_ti):
        """
        :param ing_url: 正在播放的音乐url
        :type ing_url: str
        :param so_ti: 单曲时长
        :type so_ti: str
        :return:
        :rtype:
        """
        if ing_url not in self.so_src_list:
            # 读取缓存
            cache = red_cache()
            new_li = Ui_li(cache[ing_url][0], so_ti)
            self.li[ing_url].append(new_li)
            self.verticalLayout_ing_mc_so.addWidget(self.li[ing_url][0])
            self.so_src_list.append(ing_url)
            self.updata_num()
    
    def ing_clear(self):
        try:
            fol_na = 'local'
            fi_na = 'sa_ing_li'
            obt = obt_js(fol_na, fi_na)
            for ob in obt:
                self.verticalLayout_ing_mc_so.removeWidget(self.li[ob][0])
                sip.delete(self.li[ob][0])
                del self.li[ob]
            wr_js(fol_na, fi_na, data=None)
            self.ing_clean_sign()
            self.updata_num()
        except:
            pass
        
        # self.close()
    
    # 自动加入到歌单中正在播放的歌单
    def ing_clean_sign(self):
        self.ing_clean.emit()
    
    def get_so_src_list(self):
        src_list = self.so_src_list
        self.src_list_sign.emit(src_list)
