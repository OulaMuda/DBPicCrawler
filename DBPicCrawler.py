import requests
import base64
import hashlib
import os
import urllib
import re
import configparser
import time
import random
from random import choice
from lxml import etree
import sys

#Static
Headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

#Common
Webhook = ""
ImgCacheDir = ''
StartUrl = ''
EndUrl = ''
RandPicNumMin = 0
RandPicNumMax = 0
# Webhook = ""
# ImgCacheDir = './image/img.png'
# StartUrl = '/?type=C&start='
# EndUrl = '&sortby=like&size=a&subtype=a'

#Special
PhotosUrl = []
# TotalPics = 0
# PhotosUrl = 'https://movie.douban.com/celebrity/1018562/photos'
# TotalPages = 2163 -1

def spiderDouban(in_photourl, in_starturl, in_endurl, in_totalpics):
    resource = requests.get( in_photourl+in_starturl+str(random.randint(0,in_totalpics-1))+in_endurl, headers = Headers)
    for addr in re.findall('img src=".*?"', resource.text, re.S):
        try:
            if addr.endswith(".jpg\""):
                addr = addr.replace("img src=",'')
                addr = addr.replace("\"", '')
                img_web(addr)
                break
        except requests.exceptions.ConnectionError:
            print('url error!')
            continue


#web pic
def img_web(IMAGE_URL):
    os.makedirs('./image/', exist_ok=True)

    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent','Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10')]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(IMAGE_URL, ImgCacheDir)

    with open(ImgCacheDir, 'rb') as file:  #picbase64
        data = file.read()
        encodestr = base64.b64encode(data)
        image_data = str(encodestr, 'utf-8')

    with open(ImgCacheDir, 'rb') as file:  # MD5
        md = hashlib.md5()
        md.update(file.read())
        image_md5 = md.hexdigest()

    headers = {"Content-Type": "application/json"}
    data = {
        "msgtype": "image",
        "image": {
            "base64": image_data,
            "md5": image_md5
        }
    }
    result = requests.post(Webhook, headers=headers, json=data)
    return result

def GetTotalPic(url):
    global TotalPics

    html = requests.get(url, headers = Headers).text
    s = etree.HTML(html)
    title = s.xpath('//*[@id="content"]/div/div[1]/div[2]/span[5]')
    return int(re.findall(r"\d+",title[0].text)[0])

def ReadConfig():
    global Webhook
    global ImgCacheDir
    global StartUrl
    global EndUrl
    global RandPicNumMin
    global RandPicNumMax
    global PhotosUrl

    config = configparser.ConfigParser()
    config.read(os.path.dirname(sys.argv[0])+'\Config.ini', encoding='UTF-8')

    # Terminal file path is not the same with pycharm
    # print(os.path.dirname(sys.argv[0])+'\Config.ini')
    # print(config.sections())

    Webhook = config.get('Common','Webhook')
    ImgCacheDir = config.get('Common','ImgCacheDir')
    StartUrl = config.get('Common','StartUrl')
    EndUrl = config.get('Common','EndUrl')
    RandPicNumMin = config.getint('Common','RandPicNumMin')
    RandPicNumMax = config.getint('Common','RandPicNumMax')
    PhotosUrl = config.items('DoubanPicLinks')

    return

def RandSample():
    DoubanTotaltimes = random.randint(RandPicNumMin, RandPicNumMax)
    for num in range(0, DoubanTotaltimes):
        tmpurl = choice(PhotosUrl)[1]
        spiderDouban(tmpurl, StartUrl, EndUrl, GetTotalPic(tmpurl))
    return

def PathTest():
    print("sys.path[0] = ", sys.path[0])
    print("sys.argv[0] = ", sys.argv[0])
    print("__file__ = ", __file__)
    print("os.path.abspath(__file__) = ", os.path.abspath(__file__))
    print("os.path.realpath(__file__) = ", os.path.realpath(__file__))
    print("os.path.dirname(os.path.realpath(__file__)) = ",
           os.path.dirname(os.path.realpath(__file__)))
    print("os.path.split(os.path.realpath(__file__)) = ",
           os.path.split(os.path.realpath(__file__)))
    print("os.path.split(os.path.realpath(__file__))[0] = ",
           os.path.split(os.path.realpath(__file__))[0])
    print("os.getcwd() = ", os.getcwd())

if __name__ == '__main__':
    # PathTest()
    ReadConfig()
    RandSample()



# local pic test
# def img_local(image):
#     with open(image, 'rb') as file:  #picbase64
#         data = file.read()
#         encodestr = base64.b64encode(data)
#         image_data = str(encodestr, 'utf-8')
#
#     with open(image, 'rb') as file:  # MD5
#         md = hashlib.md5()
#         md.update(file.read())
#         image_md5 = md.hexdigest()
#
#     headers = {"Content-Type": "application/json"}
#     data = {
#         "msgtype": "image",
#         "image": {
#             "base64": image_data,
#             "md5": image_md5
#         }
#     }
#     result = requests.post(url, headers=headers, json=data)
#     return result


# def spiderPicBaidu():
#     BaiduTimes = 0
#     BaiduRand = random.randint(0,29)
#     resource = requests.get('http://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&word=新垣结衣')
#     for addr in re.findall('"objURL":"(.*?)"', resource.text, re.S):
#         try:
#             if BaiduTimes == BaiduRand:
#                 img_web(addr)
#                 break
#             BaiduTimes += 1
#         except requests.exceptions.ConnectionError:
#             print('url error!')
#             continue
