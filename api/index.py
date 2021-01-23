# -*- codeing = utf-8 -*-
# @Time : 2021/01/21 9:05 上午
# @Author : Zfour
# @File : spyder1.py
# @Software : PyCharm

import leancloud
import requests
import re
from bs4 import BeautifulSoup
import time
from http.server import BaseHTTPRequestHandler

leancloud.init("LwmvjzvHzUxmJDK6QeAlflA4-MdYXbMMI", "CsDY3h7a7GYktVFH3yO8vpsd")
Aqidata = leancloud.Object.extend('aqidata')


lasttime = ''
daylist =[]

def getdata():
    r = requests.get('http://www.pm25.com/rank.html')
    r.encoding = 'utf-8'
    html = r.text
    timereg = re.compile(r'统计时间：(.*?)</span>', re.S)
    timedata = timereg.findall(html)
    datalist = []
    soup = BeautifulSoup(html, "html.parser")
    arealist = soup.find_all('ul', class_='rrank_box')
    areadata = arealist[0].find_all('li', class_='pj_area_data_item')
    for item in areadata:
        itembox = {
            "aqi":  int(item.find_all('span', class_='pjadt_aqi')[0].text),
            "area": item.find_all('a', class_='pjadt_location')[0].text
        }
        datalist.append(itembox)
    aqidata = Aqidata()
    aqidata.set('time',timedata)
    aqidata.set('data', datalist)
    query = Aqidata.query
    # 为查询创建别名
    query.descending('createdAt')
    # 选择排序方式
    query.limit(1)
    # 限定数量
    query.select('time')
    # 选择类
    lasttime = query.find()
    # 执行查询，返回数组
    if lasttime[0].get('time')[0] == timedata[0]:
        timedata[0] = "The request is repeated. The latest data is:" + timedata[0]
    else:
        aqidata.save()
    print(daylist)
    print(lasttime)
    return  timedata
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        text = getdata()
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(text[0].encode('utf-8'))
        return