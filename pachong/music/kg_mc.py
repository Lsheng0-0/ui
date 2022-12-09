# -*- coding: UTF-8 -*-
# 获取首页名称，图片，id
import configparser
import json
import os
import re
import sys
import threading
from collections import defaultdict
from time import sleep
import requests
from bs4 import BeautifulSoup

# 推荐歌单

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Connection': 'keep-alive',
    'Cookie': 'kg_mid=567828a022ecc241746477f55e63760c; '
              'ACK_SERVER_10015=%7B%22list%22%3A%5B%5B%22bjlogin-user.kugou.com%22%5D%5D%7D; '
              'kg_dfid=2mSq053VrdCs4GE8aF1hg0tJ; kg_dfid_collect=d41d8cd98f00b204e9800998ecf8427e; '
              'Hm_lvt_aedee6983d4cfc62f509129360d6bb3d=1667043965; '
              'Hm_lpvt_aedee6983d4cfc62f509129360d6bb3d=1667045140; kg_mid_temp=567828a022ecc241746477f55e63760c; '
              'KuGooRandom=66711667043976700; ACK_SERVER_10016=%7B%22list%22%3A%5B%5B%22bjreg-user.kugou.com%22%5D%5D'
              '%7D; ACK_SERVER_10017=%7B%22list%22%3A%5B%5B%22bjverifycode.service.kugou.com%22%5D%5D%7D',
    'Host': 'www.kugou.com',
    'Referer': 'https://www.kugou.com/yy/special/index/1-6-0.html',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'TE': 'trailers',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
    
}
header_img = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
}
cookies = {
    'ACK_SERVER_10015': "{\"list\":[[\"bjlogin-user.kugou.com\"]]}",
    'ACK_SERVER_10016': "{\"list\":[[\"bjreg-user.kugou.com\"]]}",
    'ACK_SERVER_10017': "{\"list\":[[\"bjverifycode.service.kugou.com\"]]}",
    'Hm_lpvt_aedee6983d4cfc62f509129360d6bb3d': "1667045422",
    'Hm_lvt_aedee6983d4cfc62f509129360d6bb3d': "1667043965",
    'kg_dfid	': "2mSq053VrdCs4GE8aF1hg0tJ",
    'kg_dfid_collect	': "d41d8cd98f00b204e9800998ecf8427e",
    'kg_mid	': "567828a022ecc241746477f55e63760c",
    'kg_mid_temp	': "567828a022ecc241746477f55e63760c",
    'KuGooRandom	': "66711667043976700",
}
params = {
    'age': '290',
    'cache-control': 'max-age=300',
    'content-encoding': 'gzip',
    'content-security-policy': "frame - ancestors 'self' *.kugou.com",
    'content-type': 'text/html;charset=utf-8',
    'date': 'Sat, 29 Oct 2022 12:10:27 GMT',
    'expires': 'Sat, 29 Oct 2022 12:10:37 GMT',
    'kg-bc-ms': '392',
    'last-modified': 'Sat, 29 Oct 2022 12:05:37 GMT',
    'server': 'kws',
    'strict-transport-security': 'max-age=604800',
    'x-content-type-options': 'nosniff',
    'X-Firefox-Spdy': 'h2',
    'x-frame-options': 'SAMEORIGIN',
    'x-via': '1.1 ong115:13 (Cdn Cache Server V2.0), 1.1 PS-KHN-01txi24:1 (Cdn Cache Server V2.0)',
    'x-ws-request-id': '635d1833_PS-KHN-01txi24_54689-30740',
}

mc_song = defaultdict(list)
mc_song_inf = defaultdict(list)


def wr_js(fol_na, fi_na, data):
    with open(r'C:\编程项目\软件项目\pachong\music\{}\{}.json'.format(fol_na, fi_na), 'w', encoding='utf-8') as f:
        # ensure_ascii=False才能输入中文，否则是Unicode字符
        # indent=2 JSON数据的缩进，美观
        json.dump(data, f, ensure_ascii=False, indent=0)
    f.close()


def red_js(fol_na, fi_na, group):
    with open(r'C:\编程项目\软件项目\pachong\music\{}\{}.json'.format(fol_na, fi_na), encoding='utf-8') as a:
        # 读取文件
        tuple = json.load(a)
        # 如果路径不存在就创建
        a.close()
        return tuple[group]


def obt_js(fol_na, fi_na):
    with open(r'C:\编程项目\软件项目\pachong\music\{}\{}.json'.format(fol_na, fi_na), encoding='utf-8') as a:
        # 读取文件
        tuple = json.load(a)
        # 如果路径不存在就创建
        a.close()
        return tuple


def red_cache():
    with open(r'pachong/music/local/cache.json', encoding='utf-8') as c:
        # 读取文件
        tuple = json.load(c)
        c.close()
        # 如果路径不存在就创建
        return tuple


# 推荐歌单 (热门)
def get_mc_sheet(url):
    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    response.close()
    reco_sheet = BeautifulSoup(response.text, "html.parser")
    reco = reco_sheet.find("ul", id="ulAlbums").find_all('li')
    for r in reco:
        re = r.find("div", class_="pic")
        # 歌单链接
        alt = re.find('img').get('alt')
        href = re.find('a').get('href')
        img = re.find('img').get('_src')
        mc_song["alt"].append(alt)
        mc_song["href"].append(href)
        mc_song["img"].append(img)
    sleep(1)


def mc_sheet_to_js(fol_na, fi_na, url):
    mc_song.clear()
    get_mc_sheet(url)  # 返回mc_reco
    wr_js(fol_na, fi_na, mc_song)
    return True


def pl_info_to_js(fol_na, fi_na):
    mc_song_inf.clear()
    href = red_js(fol_na, fi_na, 'href')
    pl_info(href)
    wr_js(fol_na, fi_na + '_inf', mc_song_inf)


# 获取歌单信息和歌曲,并写入js
def pl_info(href: list):
    while True:
        if len(href) == 0:
            break
        h = href.pop()
        # print(h)
        _inf = defaultdict(list)
        info = requests.get(h, headers=headers, cookies=cookies, params=params)  # 进行请求
        # print(info.text)
        info.close()
        info = BeautifulSoup(info.text, "html.parser")
        inf = info.find("p", class_="detail")  # 简介
        int = info.find("div", class_="intro")  # 介绍
        mc_song_inf['inf'].insert(0, inf.text.strip('\n'))
        mc_song_inf['int'].insert(0, int.text)
        song = info.find("div", id="songs").find_all('li')  # 简介
        for so in song:
            so_src = so.find('a').get('href')
            so_name = so.find('a').get('title')
            # print(so_name)
            _inf['so_src'].append(so_src)
            _inf['so_name'].append(so_name)
        mc_song_inf['song'].insert(0, _inf)
        # sleep(0.3)


def reco():
    fi_na = 'reco'
    url = 'https://www.kugou.com/yy/special/index/1-5-0.html'
    return fi_na, url


def hot():
    fi_na = 'hot'
    url = 'https://www.kugou.com/yy/special/index/1-6-0.html'
    return fi_na, url


def collection():
    fi_na = 'collection'
    url = 'https://www.kugou.com/yy/special/index/1-3-0.html'
    return fi_na, url


def rise():
    fi_na = 'rise'
    url = 'https://www.kugou.com/yy/special/index/1-8-0.html'
    return fi_na, url


def get_mp3_js(so_src):
    with open(r'pachong\music\local\cache.json', encoding='utf-8') as r:
        try:
            tuple = json.load(r)
            r.close()
            return tuple[so_src]
        except:
            r.close()
            s = get_song_page(so_src)
            if s is True:
                return True
            else:
                # 返回缓存信息，并加入缓存
                cache = nu_song_inf(so_src, s)
                if cache is not True:
                    with open(r'pachong\music\local\cache.json', 'w', encoding='utf-8') as a:
                        try:
                            tuple.update(cache)
                        
                        except:
                            tuple = cache
                        
                        json.dump(tuple, a, ensure_ascii=False, indent=-1)
                    a.close()
                    return cache[so_src]
                else:
                    return True


# 获取js的album
def get_song_page(so_src):
    # '6F64D67C0E499C0636A85807EC0F0EC5','965221','32086078',
    # 'https://wwwapi.kugou.com/yy/index.php?r=play/getdata&callback=jQuery19109016032522568235_1609768307593&hash=' + play_url_intercept_1 + '&dfid=0QqplI0WZxot12pqVh08WTx7&mid=e3a0e7839e40cf5a59a03b06b05fda0e&platid=4&album_id=' + play_url_intercept_2"
    # hash = '7A38DFB37ABF8E177E80C837C5F53DFE'
    # album_id = '4050516'
    # album_audio_id = '88547508'
    
    obj = re.compile('"hash":".*?"', re.S)
    obj2 = re.compile('"album_id":.*?,', re.S)
    obj3 = re.compile('"mixsongid":.*?,', re.S)
    # print(so_src)
    so_h5 = requests.get(so_src, headers=headers, cookies=cookies, params=params)  # 进行请求
    # print(so_h5.text)
    so_h5.close()
    so_h5_1 = obj.findall(so_h5.text)
    so_h5_2 = obj2.findall(so_h5.text)
    so_h5_3 = obj3.findall(so_h5.text)
    # print(so_h5_1)
    if len(so_h5_1) == 0:
        return True
    else:
        hash = so_h5_1[0].split(':'[-1])[1].replace('"', '')
        album_id = so_h5_2[0].split(':'[-1])[1].replace(',', '')
        album_audio_id = so_h5_3[0].split(':'[-1])[1].replace(',', '')
        # print(hash, album_id, album_audio_id)
        so_url = 'https://wwwapi.kugou.com/yy/index.php?r=play/getdata&callback=jQuery1910291402408081205_1667386744937' \
                 '&hash={}&dfid=2mSq053VrdCs4GE8aF1hg0tJ&appid=1014&mid=567828a022ecc241746477f55e63760c&platid=4' \
                 '&album_id={}&album_audio_id={}'.format(hash, album_id, album_audio_id)
        
        so_js = requests.get(so_url, headers=headers, cookies=cookies, params=params)  # 进行请求
        # 字符串处理,
        s = so_js.text.encode('utf-8').decode('unicode_escape')
        so_js.close()
        # print(s)
        
        return s


# 'http:\\singerimg.kugou.com\\uploadpic\\softhead\\400\\20221014\\20221014172236735042.jpg'
def nu_song_inf(so_src, s):
    cache = defaultdict(list)
    audio_name_1 = re.compile('"audio_name":".*?"', re.S)
    song_name_1 = re.compile('"song_name":".*?"', re.S)
    lyrics_1 = re.compile('"lyrics":".*?"', re.S)
    song_img_1 = re.compile('"img":".*?"', re.S)
    play_url_1 = re.compile('"play_url":".*?"', re.S)
    audio_name = audio_name_1.findall(s)
    song_name = song_name_1.findall(s)
    lyrics = lyrics_1.findall(s)
    play_url = play_url_1.findall(s)
    song_img = song_img_1.findall(s)
    if play_url[0].strip('play_url": ').replace('\\', '') is None:
        print('此歌曲当前不能播放')
        return True
    else:
        # 0 audio_name, 1 歌名 , 2 图片 ,3 mp3 ,4 歌词
        cache[so_src].append(audio_name[0].split(':'[-1])[1].replace('"', ''))
        cache[so_src].append(song_name[0].split(':'[-1])[1].replace('"', ''))
        cache[so_src].append(song_img[0].strip('"img":').replace('\\', '') + 'g')
        # print(song_img[0].strip('"img":').replace('\\', '')+ 'g')
        cache[so_src].append(play_url[0].strip('play_url": ').replace('\\', ''))
        ly_list = {}
        for ly in lyrics[0].replace('"', '').split('\r\n'):
            if ly == '':
                pass
            else:
                ly_ti = ly.split('[')[1].split(']')[0]
                ly_na = ly.split('[')[1].split(']')[1]
                if ly_na == '':
                    pass
                else:
                    time = int(int(ly_ti.split(':')[0]) * 60 * 1000 + float(ly_ti.split(':')[1]) * 1000)
                    ly_list[time] = ly_na.replace('\\', '')
        cache[so_src].append(ly_list)
        return cache


def add_js_data(fol_na, fi_na, tuple, data):
    with open(r'pachong\music\{}\{}.json'.format(fol_na, fi_na), 'w', encoding='utf-8') as a:
        try:
            tuple.update(data)
            print('updata')
        
        except:
            tuple = data
            print('tuple')
        
        json.dump(tuple, a, ensure_ascii=False, indent=0)
    a.close()


def to_ini(con, config, inf):
    # 修改配置文件中的信息
    proDir = os.path.dirname(os.path.realpath(sys.argv[0]))
    configPath = os.path.join(proDir, 'ui/ini/config.ini')  # 获取配置文件的路径
    conf = configparser.ConfigParser()  # 创建对象用于对配置文件进行操作
    conf.read(configPath, encoding="utf-8-sig")  # 以utf8编码形式读取
    conf.set(con, config, inf)  # 设置"config"模块下的"config"的值为"inf"
    conf.write(open(configPath, 'w+', encoding="utf-8-sig"))  # 将修改写入到配置文件


# 歌单封面下载
def dload_image(im, path, fi_na):
    image = requests.get(im, headers=header_img)  # 进行请求
    with open(r"{}/{}".format(path, fi_na), "wb") as f:
        f.write(image.content)  # 写入数据
    f.close()
    image.close()
    return True


# 歌单封面下载
def main_Downlad(mc_s: list, fi_):
    while True:
        if len(mc_s) == 0:
            break
        im = mc_s.pop()
        
        try:
            fi_na = str(len(mc_s)) + '.jpg'
            path = r'C:\编程项目\软件项目\pachong\music\img\{}'.format(fi_.split('_')[-1])
            pa = os.path.exists(path)
            if pa is not False:
                pass
            else:
                os.mkdir(path=path)
            if dload_image(im, path, fi_na):
                # print(ts_urls)
                print('线程{}正在下载章节{}'.format(threading.current_thread().getName(), im))
        except:
            print('错误：' + str(len(mc_s)) + '、' + im)


# 歌单封面下载
def Thread_dload_image(fol_na, fi_na):  # 多进程下载img
    mc_img = red_js(fol_na, fi_na, 'img')
    threading_1 = []
    for s in range(1):
        threading1 = threading.Thread(target=main_Downlad, args=(mc_img, fi_na))
        threading1.start()
        threading_1.append(threading1)
        sleep(1)
    for s in threading_1:
        s.join()
    print("<font color='blue'>" + '线程{}:已下载完成'.format(threading.current_thread().getName()) + "</font>")
    # print("<font color='blue'>" + '线程{}:已下载完成,请合并'.format(threading.current_thread().getName()) + "</font>")


def nni(in_na):
    global fi
    if in_na == 'reco':
        fi = reco()
    elif in_na == 'hot':
        fi = hot()
    elif in_na == 'collection':
        fi = collection()
    elif in_na == 'rise':
        fi = rise()
    fi_name = fi[0]
    url = fi[1]
    # 获取歌单列表信息 #fol_na=kg\reco_page fi_name = mc_{}
    fol_na = r'kg\reco_page'
    fi_na = 'mc_{}'.format(fi_name)
    mc_sheet_to_js(fol_na, fi_na, url)
    Thread_dload_image(fol_na, fi_na)
    pl_info_to_js(fol_na, fi_na)


# 飙升榜信息
def Ranking_List_js(fol_na, fi_na, src):
    
    soar_ca = defaultdict(list)
    
    response = requests.get(src, headers=headers, cookies=cookies, params=params)
    # print(response.text)
    response.close()
    soar_sheet = BeautifulSoup(response.text, "html.parser")
    soaring = soar_sheet.find("div", class_="pc_temp_songlist").find_all('ul')[0].find_all('li')
    for soar in soaring:
        url = soar.find("a", class_="pc_temp_songname").get('href')
        title = soar.find("a", class_="pc_temp_songname").get('title')
        soar_ca['alt'].append(title)
        soar_ca['href'].append(url)
    # print(soar_ca)
    wr_js(fol_na, fi_na, soar_ca)

# 排行榜主程序
def ranking_class(who):
    if who == 'soar':
        fol_na = r'kg\ranking_page'
        fi_na = '{}'.format('soar')
        src = 'https://www.kugou.com/yy/rank/home/1-6666.html?from=homepage'
        Ranking_List_js(fol_na, fi_na, src)
    elif who == 'hotsong':
        fol_na = r'kg\ranking_page'
        fi_na = '{}'.format('hotsong')
        src = 'https://www.kugou.com/yy/rank/home/1-52144.html?from=rank'
        Ranking_List_js(fol_na, fi_na, src)
    elif who == 'newsong':
        fol_na = r'kg\ranking_page'
        fi_na = '{}'.format('newsong')
        src = 'https://www.kugou.com/yy/rank/home/1-30972.html?from=rank'
        Ranking_List_js(fol_na, fi_na, src)

def down_load_mc(url_mp3,path,name_mp3):
    content3 = requests.get(url=url_mp3, headers=header_img)
    with open(r'{}\{}.mp3'.format(path, name_mp3), 'wb')as down:
        down.write(content3.content)
    down.close()

# url = 'https://webfs.ali.kugou.com/202212051406/249b130e8cf68c2feabd76635e1159f7/KGTX/CLTX003/abf1ba87b0b4126ba688e2d2125b4200.mp3'
# down_load_mc(url)
# who = 'soar'
# ranking_class(who)
# who = 'hotsong'
# ranking_class(who)
# who = 'newsong'
# ranking_class(who)


# in_na = ['reco', 'hot', 'collection', 'rise']
# for fi in in_na:
#     nni(fi)
#      ('over')
#     mc_song.clear()
#     mc_song_inf.clear()
