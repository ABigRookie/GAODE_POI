#获取边界信息
import requests
import re
import get_ip_pools as get
import random
def gethtml(url,proxy):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
        r = requests.get(url,proxies=proxy,headers=headers)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text
    except:
        return '页面获取失败'

def getedge(url,proxy):
    try:
        # proxy = random.choice(proxies)
        mes = gethtml(url,proxy)
        print(mes)
        shape = re.findall('"shape":"(.*?)",',mes)
        if shape:
            return shape[0]
        else:
            return 'null'
    except:
        return '边界获取失败'

if __name__ == '__main__':
    # print("*************正在获取IP池**************")
    # proxies = []
    # proxies = get.main_function()
    # print(proxies)
    # print("*************IP池获取完毕**************")
    proxy={'https':'https://183.129.207.78:21231'}
    url ='https://www.amap.com/detail/get/detail?id=B000A7BGMG'
    print(getedge(url,proxy))