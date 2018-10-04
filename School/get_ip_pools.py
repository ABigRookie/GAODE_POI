import sqlite3
from urllib.request import urlopen
import re
import requests
from bs4 import BeautifulSoup as bs
from urllib import request
import socket
from multiprocessing import Pool
import time

#超时时间设置为 3 秒
socket.setdefaulttimeout(3)


#测试ip是否可用的测试网址
test_url = "https://www.baidu.com/"


#发送请求获取ip列表
def request_to_get(url):
    header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Host": "www.xicidaili.com",
        "Referer": "http://www.xicidaili.com/",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    }
    response = requests.get(url, headers=header).content
    content = str(response, encoding="utf-8")
    bs_obj = bs(content, "html.parser")
    return bs_obj


#获取IP及其端口，并转换成统一格式{"http": "http://" + ip_list[i] + ":" + port_list[i]}
def find_ip_port(bs_obj):
    ip_list = []
    port_list = []
    ips = bs_obj.findAll('tr')
    for x in range(1, len(ips)):
        ip = ips[x]
        tds = ip.findAll("td")
        ip_list.append(tds[1].text)
        port_list.append(tds[2].text)
    proxys = []
    for i in range(len(ip_list)):
        proxy_host = "http://" + ip_list[i] + ":" + port_list[i]
        proxy_temp = {"http": proxy_host}
        proxys.append(proxy_temp)
    return proxys


#检查ip是否可用
def check_ip(proxy):
    try:
        response = requests.get(test_url,proxies=proxy,timeout=2)
        if response.status_code==200:
            return proxy
    except:
        pass



#测试并返回可用的ip列表
def return_ok_proxys(proxys):
    pool = Pool(processes=4)
    alright_proxys = []
    msgs = [i for i in proxys]
    alright_proxys = pool.map(check_ip,msgs)
    pool.close()
    pool.join()
    return alright_proxys


# main function
def main_function():
    IP_Page = 100
    proxys=[]
    alright_proxys=[]
    for i in range(1,3):
        time.sleep(3)
        url = "http://www.xicidaili.com/nn/" + str(i)
        bs_obj = request_to_get(url)
        proxys.extend(find_ip_port(bs_obj))
    alright_proxys=return_ok_proxys(proxys)
    return alright_proxys