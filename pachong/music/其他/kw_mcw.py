import json
import os
import threading
from collections import defaultdict
from time import sleep
import requests
# 发送请求时的头文件
from bs4 import BeautifulSoup

mc_sheet_all = defaultdict(list)


# 获取首页名称，图片，id
def get_cloud_sheet(ty, num):
    # 先对首页进行简单处理
    
    url2 = 'https://music.163.com/discover/playlist/?order=hot&cat={}&limit=35&offset={}'.format(ty, num)
    response = requests.get(url2, headers=headers, cookies=cookies, params=params)
    response.close()
    # print(response.text)
    cloud_sheet = BeautifulSoup(response.text, "html.parser")
    cloud_li = cloud_sheet.find("ul", class_="m-cvrlst f-cb").find_all('li')
    # resp = obj1.findall(response.text)
    for l in cloud_li:
        # print(l)
        img_sheet = l.find('img').get('src')
        # print(img_sheet.split('?')[0])
        id_sheet = l.find('a').get('href')
        ti_sheet = l.find('a').get('title')
        # print(id_sheet, ti_sheet)
        mc_sheet_all["href"].append(id_sheet)
        mc_sheet_all["title"].append(ti_sheet)
        mc_sheet_all["img"].append(img_sheet.split('?')[0])


def mc_str_all(ty, num, filename):
    n = 0
    for i in range(num):
        get_cloud_sheet(ty, n * 35)
        n = n + 1
        # print(n)
        sleep(1)
    
    with open('mc_sheet_{}.json'.format(filename), 'w', encoding='utf8') as f:
        # ensure_ascii=False才能输入中文，否则是Unicode字符
        # indent=2 JSON数据的缩进，美观
        json.dump(mc_sheet_all, f, ensure_ascii=False, indent=0)
    f.close()
    del mc_sheet_all[:]


# ty = '全部'
# num = 18
# mc_str_all(ty, num)
def red_json(file_na, vue):
    with open('mc_sheet_{}.json'.format(file_na), encoding='utf-8') as a:
        # 读取文件
        mc_sheet = json.load(a)
        # 如果路径不存在就创建
        return mc_sheet[vue]


def download_file(im, path, n):
    
    image = requests.get(im, headers=mc_im_header)  # 进行请求
    # print(image.text)
    with open("{}/{}".format(path, n), "wb") as f:
        f.write(image.content)  # 写入数据
    f.close()
    image.close()
    print("下载完毕：" + im)
    return True


# 下载首页推荐歌单封面
def down_mc_img(mc_s: list, file_na):
    i = len(mc_s)
    while True:
        if len(mc_s) == 0:
            break
        im = mc_s.pop()
        try:
            n = str(i) + '.jpg'
            path = os.path.join('img/' + file_na)
            pa = os.path.exists(path)
            if pa is not False:
                pass
            else:
                os.mkdir(path=path)
            
            if download_file(im, path, n):
                # print(ts_urls)
                print('线程{}正在下载章节{}'.format(threading.current_thread().getName(), im))
        except:
            print('错误：' + str(i) + '、')
            # print('错误：' + str(i) + '、' + mc_s[i])
        i = i - 1
        # sleep(1)


def down_mc_img_Thread(mc_s, file_na):  # 多进程下载img
    threading_1 = []
    for i in range(30):
        threading1 = threading.Thread(target=down_mc_img, args=(mc_s, file_na))
        threading1.start()
        threading_1.append(threading1)
        sleep(1)
    for i in threading_1:
        i.join()
    print(' 当前线程为{}'.format(threading.current_thread().getName()))


# 下载首页推荐歌单封面
# file_na = 'all'
# mc_s = red_json(file_na,'img')
# down_mc_img_Thread()

st_song = defaultdict(list)


# 通过歌单playlist_id获取歌单信息
def playlist_info(_id: list, _ti: list):
    mc_song = defaultdict(list)
    url = "https://music.163.com" + str(_id)
    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    # print(response.text)
    introduce = BeautifulSoup(response.text, "html.parser")
    intr = introduce.find("p", class_="intr f-brk f-hide")
    # print(intr)
    # title = BeautifulSoup(response.text, "html.parser")
    # title = title.find("h2", class_="f-ff2 f-brk")
    # # print(title.text)
    song = BeautifulSoup(response.text, "html.parser")
    table = song.find("ul", class_="f-hide").find_all('li')
    if intr is None:
        intr = '本作者太懒,没有介绍'
        mc_song['intr'].append(intr)
    else:
        mc_song['intr'].append(intr.text)
    for ta in table:
        da = ta.find('a').get('href')
        na = ta.text
        # print(da, na)
        mc_song['song_id'].append(da)
        mc_song['song_name'].append(na)
    
    st_song[_ti].append(mc_song)


# 保存到js
def js_plist():
    _id = red_json('all', 'href')
    _ti = red_json('all', 'title')
    n = 0
    for i in _id:
        playlist_info(i, _ti[n])
        n = n + 1
    with open('mc_sheet_{}.json'.format('st_song'), 'w', encoding='utf8') as f:
        # ensure_ascii=False才能输入中文，否则是Unicode字符
        # indent=2 JSON数据的缩进，美观
        json.dump(st_song, f, ensure_ascii=False, indent=0)
        f.close()
js_plist()
# # 传入dj电台的id号，获取dj电台的音频文件
# def dj_url(dj_id):
#     url = "https://api.imjad.cn/cloudmusic/?type=dj&id=" + dj_id
#     response = requests.get(url, headers=heades[random.randint(0, len(heades) - 1)]).json()
#     return response['data'][0]['url']
#
#
# # 通过指定的歌曲song_id获取歌曲的音频二进制文件
# def song_url(song_id, br=320000):
#     # 通过urls获取歌曲下载链接
#     urls = "https://api.imjad.cn/cloudmusic/?type=song&id={}&br={}".format(song_id, br)
#     url = requests.get(urls).json()['data'][0]['url']
#     return url
#
#
# # 单曲搜索
# def single_search(name):
#     song_name, song_id, singer = [], [], []
#     url = "http://music.163.com/api/search/get/web?csrf_token=hlpretag=&hlposttag=&s={" + name + "}&type=1&offset=0&total=true&limit=30"
#     data = requests.get(url, headers=heades[random.randint(0, len(heades) - 1)])
#     songs = data.json()['result']['songs']
#     for i in songs:
#         song_name.append(i['name'] + "  <-歌手-->  " + i['artists'][0]['name'])
#         song_id.append(str(i['id']))
#     return song_name, song_id
#
#
# if __name__ == '__main__':
#     url = "https://api.imjad.cn/cloudmusic/?type=song&id=1809318575&br=320000"
