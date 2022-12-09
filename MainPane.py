import configparser
import os
import sys
import threading
from datetime import datetime, timedelta

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QPoint, QFileInfo, QUrl
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtWebEngineWidgets import QWebEngineView

from pachong.music.kg_mc import wr_js
from page.api_page import api_Page
from page.music.mc_main_page import mc_p_Switch
from thread_mc.thread_mc import re_js_thread
from ui.api_windows.ui_exit import ui_exit
from ui.api_windows.ui_mp3_player import ui_mp3
from ui.main_window import Ui_MainWindow
from ui.template.local_mc_list import Ui_local_mc_list
from ui.template.scroll_text import ScrollTextWindow


class MainPane(mc_p_Switch, api_Page, ui_exit):
    mian_m_Position = pyqtSignal()
    
    def __init__(self):
        super(MainPane, self).__init__()
        
        # 将UI界面布局到Demo上；
        # 初始化
        self.last_ini = None
        global order
        order = []
        self.ui = Ui_MainWindow()
        self.api_P = api_Page()
        self.exit = ui_exit()
        self.mc_p_Switch = mc_p_Switch()
        self.lock = threading.Lock()  # 数据锁
        self.player = QMediaPlayer()  # 音乐播放器
        self.player.setVolume(50)  # 设置初始播放音量
        self.time = QTimer()  # 设置一个定时器
        self.time.start(1000)  # 定时一秒
        self.several = 0
        self.setime = QTimer()  # 设置一个定时器
        self.setime.start(1000)  # 定时一秒
        
        self.setupUi(self)
        self.retranslateUi(self)
        self.initUI()
        
        # 需要提前加载的数据
        self.read_ini_conf()
        
        # 信号量与槽信号绑定
        self.pushButton_top_6_close.clicked.connect(lambda: self.close_change())  # 关闭窗口
        self.pushButton_top_6_size.clicked.connect(lambda: self.slot_max_or_recv())  # 最大化窗口
        self.pushButton_top_6_hide.clicked.connect(lambda: self.showmin_even())  # 最小化窗口
        
        self.pushButton_bottom_ini_logo.clicked.connect(lambda: self.bt_page_music_alone())  # 左下角旋钮切换
        self.pushButton_bottom_button_1_down.clicked.connect(lambda: self.bt_page_music_alone_out())  # 切换回来
        
        # play
        self.time.timeout.connect(lambda: self.timeout_process())  # 计时时间到了以后的处理函数
        self.setime.timeout.connect(lambda: self.play_label())  # 轮播文字的处理
        self.horizontalSlider.valueChanged.connect(lambda: self.volume_adjust())  # 拖动音量条改变音量
        self.horizontalSlider_speed.sliderMoved.connect(lambda: self.music_time_adjust())  # 拖动进度条改变播放进度
        self.horizontalSlider_speed.sliderReleased.connect(
                lambda: self.music_time_adjust_over()
        )  # 拖动进度条调整完成，拖动调节分成两步，播放本地音乐时可去除杂音
        self.pushButton_bottom_playbar_pattern.clicked.connect(lambda: self.bt_playbar_pattern())  # 循环播放策略
        self.pushButton_bottom_menu.clicked.connect(lambda: self.bt_mc_menu())  # 正在播放的列表，播放即加入列表
        self.pushButton_bottom_play.clicked.connect(lambda: self.bt_bottom_play())  # 下方播放按钮
        self.pushButton_bottom_next.clicked.connect(lambda: self.next_music())  # 下一首
        self.pushButton_bottom_last.clicked.connect(lambda: self.last_music_thread())  # 上一首
        self.pushButton_bottom_lyric.clicked.connect(lambda: self.mp3_player())  # mp3
        self.pushButton_bottom_button_1_download.clicked.connect(lambda: self.bt_download())
        
        # 主页
        self.pushButton_top_1.clicked.connect(lambda: self.bt_page_index())
        self.pushButton_top_2_left.clicked.connect(lambda: self.bt_page_left())
        self.pushButton_top_2_right.clicked.connect(lambda: self.bt_page_right())
        # 音乐专栏
        self.pushButton_music_1.clicked.connect(lambda: self.set_index_thread())
        self.pushButton_music_2.clicked.connect(lambda: self.bt_page_music_local())
        self.pushButton_music_3.clicked.connect(lambda: self.bt_page_music_localbrowse())
        self.pushButton_tab_reco_music_Refresh.clicked.connect(lambda: self.refresh_index())
        # 全部
        self.pushButton_tab_index_music_m_m_2.clicked.connect(lambda: self.bt_page_music_all())
        self.pushButton_tab_index_music_m_m_3.clicked.connect(lambda: self.bt_page_music_chinese())
        self.pushButton_tab_index_music_m_m_4.clicked.connect(lambda: self.bt_page_music_europe())
        self.pushButton_tab_index_music_m_m_5.clicked.connect(lambda: self.bt_page_music_korea())
        self.pushButton_tab_index_music_m_m_6.clicked.connect(lambda: self.bt_page_music_japan())
        self.pushButton_tab_index_music_m_m_7.clicked.connect(lambda: self.bt_page_music_minor())
        self.m_flag = False
        self.p_path = self.get_ini('mc_pathEd_for', 'p_path')
        self.path_La.setText(self.p_path)
        self.ping_path = self.get_ini('mc_pathIng_for', 'p_path')
        self.path_LA.setText(self.ping_path)
        self.file_path = self.get_ini('file_path', 'p_path')
        self.mc_local_list = []
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标
    
    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            try:
                m_P = QMouseEvent.globalPos() - self.m_Position
                _ing = QPoint(710, 65)
                _exit = QPoint(324, 219)
                self.ing_mc.move(m_P + _ing)
                self.exit.move(m_P + _exit)
            except:
                pass
            QMouseEvent.accept()
    
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))
    
    # 关闭窗口改写(下次不在提醒将无弹窗出现,直接关闭)
    def close_change(self):
        global order
        if len(order) == 1:
            return self.colse_pa()
        else:
            order = ['one']
        if self.so_serial == 1:
            self.ing_mc.close()
            self.so_serial = 0
        self.exit.show()
        self.exit.pushButton_exit_2_2.clicked.connect(lambda: self.exit_close())
        close = self.get_ini('close', 'close')
        if close == 'yes':
            self.colse_pa()
        elif close == 'no':
            self.exit.pushButton_exit_ok.clicked.connect(lambda: self.colse_even())
    
    # 重写最小化窗口
    def showmin_even(self):
        if self.so_serial == 1:
            self.ing_mc.close()
            self.so_serial = 0
        self.showMinimized()
    
    # 改写关闭策略
    def colse_even(self):
        if self.exit.radioButton_exit_2.isChecked():
            if self.exit.checkBox_exit.isChecked():
                self.to_ini('close', 'close', 'yes')  # 不再提醒写入关闭配置文件
            else:
                pass
            self.colse_pa()
        elif self.exit.radioButton_exit.isChecked():
            self.showmin()
            global order
            order = []
    
    # 弹窗关闭
    def exit_close(self):
        self.exit.close()
        global order
        order = []
    
    # 关闭窗口和弹窗
    def colse_pa(self):
        self.exit.close()
        self.close()
    
    # 关闭弹窗，最小换窗口
    def showmin(self):
        self.exit.close()
        self.showMinimized()
    
    # 最大化按钮变换
    def slot_max_or_recv(self):
        if self.isMaximized():
            if self.so_serial == 1:
                self.ing_mc.close()
                self.so_serial = 0
            self.showNormal()
            self.pushButton_top_6_size.setIcon(QtGui.QIcon(':/icon/icon/big.png'))  # 设置图标
        else:
            if self.so_serial == 1:
                self.ing_mc.close()
                self.so_serial = 0
            self.showMaximized()
            self.pushButton_top_6_size.setIcon(QtGui.QIcon(':/icon/icon/low.png'))  # 设置图标
    
    def get_ini(self, con, config):
        proDir = os.path.dirname(os.path.realpath(sys.argv[0]))
        configPath = os.path.join(proDir, 'ui/ini/config.ini')  # 获取配置文件的路径
        conf = configparser.ConfigParser()  # 创建对象用于对配置文件进行操作
        conf.read(configPath, encoding="utf-8-sig")  # 以utf8编码形式读取
        pat = conf.get(con, config)  # 读取配置文件设置的语言的值
        return pat
    
    def to_ini(self, con, config, inf):
        # 修改配置文件中的信息
        proDir = os.path.dirname(os.path.realpath(sys.argv[0]))
        configPath = os.path.join(proDir, 'ui/ini/config.ini')  # 获取配置文件的路径
        conf = configparser.ConfigParser()  # 创建对象用于对配置文件进行操作
        conf.read(configPath, encoding="utf-8-sig")  # 以utf8编码形式读取
        conf.set(con, config, inf)  # 设置"config"模块下的"config"的值为"inf"
        conf.write(open(configPath, 'w+', encoding="utf-8-sig"))  # 将修改写入到配置文件
    
    def read_ini_conf(self):
        # 需要提前加载的数据
        pat = self.get_ini('pattern', 'pattern')
        self.pushButton_bottom_playbar_pattern.setObjectName(pat)  # 循环播放
        self.pushButton_bottom_playbar_pattern.setIcon(QtGui.QIcon(':/icon/icon/{}.png'.format(pat)))  # 设置图标
    
    def timr_update(self):
        # 时间大于1天重新缓存(网站mp3音频文件会随更新时间重定向)
        now = datetime.now()
        now_StyleTime = now.strftime("%Y-%m-%d %H:%M:%S")
        now.date()
        last_date = self.get_ini('last_data', 'datetime')
        date_last_date = datetime.strptime(last_date, "%Y-%m-%d %H:%M:%S")
        print(last_date)
        addDays = (date_last_date + timedelta(days=1))  # 加1天
        if addDays > now:
            print(addDays > now)
        else:
            self.to_ini('last_data', 'datetime', now_StyleTime)
            wr_js(r'local', 'cache', None)
    
    def initUI(self):
        self.setWindowTitle('播放器v2.0')
        self.setWindowIcon(QIcon(':/icon/icon/logo.png'))
        self.setWindowOpacity(1)  # 设置窗口透明度
        self.setAttribute(Qt.WA_TranslucentBackground)  # 窗体背景透明
        self.setWindowFlags(Qt.FramelessWindowHint)  # 窗口置顶，无边框
        
        self.pushButton_bottom_play.setObjectName('play')
        
        # 实例化web小部件
        # self.browser = QWebEngineView()
        # self.browser.load(QUrl(QFileInfo("ceshi.html").absoluteFilePath()))
        
        # 加载外部的web界面
        # self.browser.load(QUrl('https://www.kugou.com/mixsong/j3pry11.html'))
        # self.mc_loaded_list_song_SA.setWidget(self.browser)

        # 推荐
        self.pushButton_tab_reco_music_reco.clicked.connect(lambda: self.set_reco_thread())
        self.pushButton_tab_reco_music_hot.clicked.connect(lambda: self.set_hot_thread())
        self.pushButton_tab_index_music_collection.clicked.connect(lambda: self.set_collection_thread())
        self.pushButton_tab_index_music_rise.clicked.connect(lambda: self.set_rise_thread())
        
        self.label_bottom_ini = '暂无播放'
        self.label_bottom_ini_name = '未知歌曲'
        

        self.mc_manage_loading_Bt.clicked.connect(lambda: self.mc_Mg_loading_Bt())
        self.mc_manage_loaded_Bt.clicked.connect(lambda: self.mc_Mg_loaded_Bt())
        self.path_Bt.clicked.connect(lambda: self.mc_pathEd_Bt())
        self.path_BT.clicked.connect(lambda: self.mc_pathIng_Bt())
        self.file_Path.clicked.connect(lambda: self.file_Path_Bt())

    def sign_so_detail_page(self):
        if self.page_last == 0:
            pass
        else:
            for i in range(abs(self.page_last) - 1):
                self.page_index_num.pop()
                print(self.page_index_num)
        get_page = self.get_sWidget_main()
        self.so_detail = get_page
        self.page_last = 0
        self.page_index_num.append(self.so_detail)
    
    '''主界面窗口'''
    
    def sWidget_main(self, p):
        try:
            if self.so_serial == 1:
                self.ing_mc.close()
        except:
            pass
        self.stackedWidget_main.setCurrentIndex(p)
    
    '''中间全部界面窗口'''
    
    def sWidget_middle(self, p):
        try:
            if self.so_serial == 1:
                self.ing_mc.close()
        except:
            pass
        self.stackedWidget_frame_middle.setCurrentIndex(p)

    '''本地音乐下载音乐'''
    def sWidget_local(self, p):
        try:
            if self.so_serial == 1:
                self.ing_mc.close()
        except:
            pass
        self.mc_manage_load_SW.setCurrentIndex(p)
    '''底部两个界面'''
    
    def sWidget_bt(self, p):
        try:
            if self.so_serial == 1:
                self.ing_mc.close()
        except:
            pass
        self.stackedWidget_bottom.setCurrentIndex(p)
    
    '''获取当前页面 num'''
    
    def get_sWidget_main(self):
        get_num = self.stackedWidget_main.currentIndex()
        return get_num
    
    '''获取推荐歌单的 num'''
    
    def get_sWidget_reco(self):
        get_num = self.stackedWidget_mc_reco_reco.currentIndex()
        return get_num
    
    def set_index_thread(self):
        self.index_js = re_js_thread()
        self.index_js.sinout.connect(self.bt_page_music_index)
        self.index_js.set_param(r'kg\reco_page', 'mc_reco', 'alt')
        self.index_js.start()
    
    def set_reco_thread(self):
        self.reco_js = re_js_thread()
        self.reco_js.sinout.connect(self.bt_page_music_reo)
        self.reco_js.set_param(r'kg\reco_page', 'mc_reco', 'alt')
        self.reco_js.start()
    
    def set_hot_thread(self):
        self.hot_js = re_js_thread()
        self.hot_js.sinout.connect(self.bt_page_music_hot)
        self.hot_js.set_param(r'kg\reco_page', 'mc_hot', 'alt')
        self.hot_js.start()
    
    def set_collection_thread(self):
        self.coll_js = re_js_thread()
        self.coll_js.sinout.connect(self.bt_page_music_collection)
        self.coll_js.set_param(r'kg\reco_page', 'mc_collection', 'alt')
        self.coll_js.start()
    
    def set_rise_thread(self):
        self.rise_js = re_js_thread()
        self.rise_js.sinout.connect(self.bt_page_music_rise)
        self.rise_js.set_param(r'kg\reco_page', 'mc_rise', 'alt')
        self.rise_js.start()
    
    # mp3小组件
    def mp3_player(self):
        self.hide()
        self.mp3 = ui_mp3(parent=self)
        try:
            if self.so_serial == 1:
                self.ing_mc.close()
        except:
            pass
        self.mp3.show()
        self.mp3_inherit_main()
        
        if self.mp3.exec():
            pass  # do stuff on success
        self.show()
    
    # 继承主菜单的函数到mp3
    def mp3_inherit_main(self):
        self.mp3.mp3_play_bt.connect(self.bt_bottom_play)  # mp3播放按钮的信号和槽
        self.mp3.mp3_next_bt.connect(lambda: self.next_music())  # 下一首
        self.mp3.mp3_last_bt.connect(lambda: self.last_music_thread())  # 上一首
        self.mp3.mp3_pattern_bt.connect(lambda: self.bt_playbar_pattern())  # 循环播放策略
        # mp3 的暂停变化
        self.mp3.mp3_information_logo_Bt.setStyleSheet(self.pushButton_bottom_ini_logo.styleSheet())
        self.mp3.mp3_player_play_Bt.setObjectName(self.pushButton_bottom_play.objectName())
        self.mp3.mp3_player_play_Bt.setIcon(self.pushButton_bottom_play.icon())  # 设置图标
        self.mp3.mp3_player_pattern_Bt.setIcon(self.pushButton_bottom_playbar_pattern.icon())
        self.mp3.mp3_player_pattern_Bt.setObjectName(self.pushButton_bottom_playbar_pattern.objectName())
        # Label
        self.mp3.mp3_time_pre_L.setText(self.label_time_pre.text())
        self.mp3.mp3_time_so_L.setText(self.label_time_next.text())  # 设置音频长度的显示
        # 实例化小部件的滚动字幕
        try:
            self.mp3.horizontalLayout_3.removeWidget(self.scrollTextWindow_mp3)
        except:
            pass
        self.scrollTextWindow_mp3 = ScrollTextWindow(self.label_bottom_ini, self.label_bottom_ini_name, 8, 12, self)
        self.mp3.horizontalLayout_3.addWidget(self.scrollTextWindow_mp3)
    
    # 轮播label
    def play_label(self):
        if self.last_ini != self.label_bottom_ini:
            self.several = 0
        if len(self.label_bottom_ini) > 30:
            self.label__page_music_user.setText("{}".format(self.label_bottom_ini[self.several:self.several + 30]))
            self.several += 1
            if self.several == len(self.label_bottom_ini) - 30:
                self.several = 0
        else:
            self.label__page_music_user.setText("{}".format(self.label_bottom_ini[self.several:self.several + 30]))
        self.last_ini = self.label_bottom_ini
