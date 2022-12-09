# !/usr/bin/env python
# -*- coding: UTF-8 -*-
from PyQt5.QtCore import QThread, pyqtSignal, QMutex
from pachong.music.kg_mc import red_js, obt_js, red_cache, get_mp3_js, reco, hot, collection, rise, mc_sheet_to_js, \
    Thread_dload_image, pl_info_to_js, down_load_mc

qmut_1 = QMutex()  # 创建线程锁
qmut_2 = QMutex()
qmut_4 = QMutex()
qmut_5 = QMutex()
qmut_6 = QMutex()
qmut_7 = QMutex()
qmut_8 = QMutex()

class re_js_thread(QThread):
    sinout = pyqtSignal(list)  # 自定义信号，执行run()函数时，从相关线程发射此信号
    
    def __init__(self):
        super(re_js_thread, self).__init__()
        self.group = None
        self.fi_na = None
        self.fol_na = None
    
    def set_param(self, fol_na, fi_na, group):
        self.fol_na = fol_na
        self.fi_na = fi_na
        self.group = group
    
    def run(self):
        qmut_1.lock()
        try:
            alt = red_js(self.fol_na, self.fi_na, self.group)
            self.sinout.emit(alt)
        except:
            pass
        qmut_1.unlock()


class set_songlist_page_Th(QThread):
    toout = pyqtSignal(str, str, str, str, list)  # 自定义信号，执行run()函数时，从相关线程发射此信号
    
    def __init__(self):
        super(set_songlist_page_Th, self).__init__()
        self.alt_na = None
        self.fol_na = None
        self.na = None
        self.num = None
        self.fi_na = None
    
    def set_param(self, fol_na, fi_na, na, num, alt_na):
        self.na = na
        self.fol_na = fol_na
        self.fi_na = fi_na
        self.num = num
        self.alt_na = alt_na
    
    def run(self):
        qmut_2.lock()
        obt = obt_js(self.fol_na, self.fi_na)
        grid_na = self.na + '_' + str(self.num)
        inf = obt['inf']
        iny = obt['int']
        song = obt['song']
        inf_iny = inf[self.num] + '\n' + iny[self.num]
        so_name = song[self.num]['so_name']
        im_path = 'pachong/music/img/{}/{}.jpg'.format(self.na, self.num)
        self.toout.emit(grid_na, im_path, self.alt_na, inf_iny, so_name)
        qmut_2.unlock()


class re_so_ing_thread(QThread):
    toout = pyqtSignal(list, list, list)  # 自定义信号，执行run()函数时，从相关线程发射此信号
    sinout = pyqtSignal(list, list, list, list)
    
    def __init__(self):
        super(re_so_ing_thread, self).__init__()
    
    def run(self):
        global mp3_li
        qmut_4.lock()
        lsr = []
        lo = []
        lo_ti = []
        lo_num = []
        lo_cl = []
        fol_na = 'local'
        fi_na = 'sa_ing_li'
        try:
            obt = obt_js(fol_na, fi_na)
            for ob in obt:
                try:
                    cache = red_cache()
                    if len(cache[ob]) != 0:
                        mp3_li = cache[ob]
                except:
                    mp3_li = get_mp3_js(ob)
                
                if mp3_li is True:
                    print('此歌曲当前查询不到')
                else:
                    lo.append(mp3_li)
                    lsr.append(ob)
                    lo_ti.append(obt[ob][2])
                    lo_cl.append(obt[ob][0])
                    lo_num.append(obt[ob][1])
        
        except:
            pass
        self.toout.emit(lo, lsr, lo_ti)
        self.sinout.emit(lsr, lo_cl, lo_num, lo)
        qmut_4.unlock()


class add_list_thread(QThread):
    toout = pyqtSignal(list)  # 自定义信号，执行run()函数时，从相关线程发射此信号
    
    def __init__(self):
        super(add_list_thread, self).__init__()
        self.no = None
        self.nu = None
        self.cl_pa = None
    
    def set_param(self, cl_pa,no):
        self.cl_pa = cl_pa
        self.no = no
    
    def run(self):
        qmut_5.lock()
        add_list = []
        na = self.cl_pa.split('_')[0]
        num = int(self.cl_pa.split('_')[-1])
        sr = red_js(r'kg\reco_page', 'mc_{}_inf'.format(na), 'song')
        so_src = sr[num]['so_src']
        li_na = na + '_' + str(num)
        for i in self.no:
            add_list.append([li_na, i, so_src[i]])
        self.toout.emit(add_list)
        qmut_5.unlock()


class add_ranking_thread(QThread):
    toout = pyqtSignal(list)  # 自定义信号，执行run()函数时，从相关线程发射此信号
    
    def __init__(self):
        super(add_ranking_thread, self).__init__()
        self.cl_pa = None
    
    def set_param(self, cl_pa):
        self.cl_pa = cl_pa
    
    def run(self):
        qmut_7.lock()
        add_list = []
        so_src = red_js(r'kg\ranking_page', self.cl_pa, 'href')
        for i in range(len(so_src)):
            add_list.append([self.cl_pa, i, so_src[i]])
        self.toout.emit(add_list)
        qmut_7.unlock()
class refresh_thread(QThread):
    toout = pyqtSignal()  # 自定义信号，执行run()函数时，从相关线程发射此信号
    
    def __init__(self):
        super(refresh_thread, self).__init__()
    
    def set_param(self, in_na):
        self.in_na = in_na
    
    def run(self):
        global fi
        qmut_6.lock()
        if self.in_na == 'reco':
            fi = reco()
        elif self.in_na == 'hot':
            fi = hot()
        elif self.in_na == 'collection':
            fi = collection()
        elif self.in_na == 'rise':
            fi = rise()
        fi_name = fi[0]
        url = fi[1]
        # 获取歌单列表信息 #fol_na=kg\reco_page fi_name = mc_{}
        fol_na = r'kg\reco_page'
        fi_na = 'mc_{}'.format(fi_name)
        mc_sheet_to_js(fol_na, fi_na, url)
        Thread_dload_image(fol_na, fi_na)
        pl_info_to_js(fol_na, fi_na)
        self.toout.emit()
        qmut_6.unlock()


class dload_mp3_thread(QThread):
    mp3_out = pyqtSignal(str,list,int)  # 自定义信号，执行run()函数时，从相关线程发射此信号
    
    def __init__(self):
        super(dload_mp3_thread, self).__init__()
        self.num = None
        self.url = None

    def set_param(self, url, num):
        self.url = url
        self.num = num
    def run(self):
        global fi
        qmut_8.lock()
        try:
            cache = red_cache()
            if len(cache[self.url]) != 0:
                self.mp3 = cache[self.url]
        except:
            self.mp3 = get_mp3_js(self.url)
        if self.mp3 is True:
            print('此歌曲当前无法下载,点击下面链接手动解锁滑块')
            print(
                    'https://www.kugou.com/mixsong/j3pry11.html#hash=6F64D67C0E499C0636A85807EC0F0EC5&album_id=965221&album_audio_id=32086078'
            )
            self.mp3 = None
            self.num = None
        self.mp3_out.emit(self.url, self.mp3, self.num)
        qmut_8.unlock()
