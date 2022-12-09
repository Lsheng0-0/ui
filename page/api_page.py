# -*- coding: UTF-8 -*-
from PyQt5.QtWidgets import QMainWindow
from ui.main_window import Ui_MainWindow

'''
frame_tab_index_music_m_table:
0 全部
1 华语
2 欧美
3 韩国
4 日本
5 小语种


'''


class api_Page(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(api_Page, self).__init__()
        # 将UI界面布局到Demo上；

    '''音乐推荐表单'''
    
    def sWidget_ip_mc(self, p):
        self.stackedWidget_tab_index_music_m_table.setCurrentIndex(p)
    
    '''推荐歌单'''
    
    def sWidget_reo_mc(self, p):
        self.stackedWidget_mc_reco_reco.setCurrentIndex(p)
    
    # 最近浏览
    def bt_page_music_all(self):
        self.sWidget_ip_mc(0)
    
    def bt_page_music_chinese(self):
        self.sWidget_ip_mc(1)
    
    def bt_page_music_europe(self):
        self.sWidget_ip_mc(2)
    
    def bt_page_music_korea(self):
        self.sWidget_ip_mc(3)
    
    def bt_page_music_japan(self):
        self.sWidget_ip_mc(4)
    
    def bt_page_music_minor(self):
        self.sWidget_ip_mc(5)
