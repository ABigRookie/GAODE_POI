#本文件进行高德地图的景点POI信息获取
import requests
import re
import csv
from multiprocessing import Pool
import time
import get_ip_pools as get
import random

#获取详细边界信息
def getedge(IDlist,proxies):
    try:
        shapes=[]
        for id in IDlist:
            proxy = random.choice(proxies)
            url = 'https://www.amap.com/detail/get/detail?id='+str(id)
            header = {
                "Cookie":'Cookie: guid=8fad-e1ec-039c-7162; UM_distinctid=164f3323b4e31-0fe089552c94db-f373567-1fa400-164f3323b4f1af; cna=ggNqEjFUsjoCAXaQhSTRVSfa; _uab_collina=153370435036652277261537; passport_login=MjA4NzEyNzQ3LGFtYXBfMTU4MDE2MjY4MzZBaTBEZ29rNTUscWd1dGY5c3p0YTY4amQ5MWVwcnJ0MGs1NHB3Z2p6OXosMTUzMzcwNDYyMixOakF5Wm1aak5qYzVOMlF6WVRRelkyRXhPRFl3TXpFMVpEQmxaR0l6WkdRPQ%3D%3D; dev_help=nCydfSBPBjJNGX6opEOYP2I3NWE3Njg3MzE1ZGFhMTRkNTg5ODgxODE0ZDQ4ZGJkNThkZGExMGE2YjZkZmM5MDhhOWQyMTgxNTQ3M2VjN2VCK8MbQf3Qbzcrr5M0CWmiW99yHV1MaKzs5LZJKOTUnSFh%2Fy8MVteprFV34%2B3abUosZH9AqMU%2B3cRJZJhHrE6p%2Fwq%2B%2BCenOC6RZCi0OjwkXhEwlRjX7Gni43EZWO%2FcZrQ36ByYeO0Kbhqp9EfwlMTH; key=bfe31f4e0fb231d29e1d3ce951e2c780; CNZZDATA1255626299=214960262-1533700612-https%253A%252F%252Fwww.baidu.com%252F%7C1535865709; isg=BHFxLZxNjot6pyJ-u6s_jS67gP3L9uV0Ke0JDFOGbThXepHMm671oB-4mE65qX0I',
                "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36",
            }
            r = requests.get(url,proxies=proxy,headers=header)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            mes = r.text
            shape=re.findall('"shape":"(.*?)",',mes)
            if shape:
                b = shape[0].replace(';', '],[')
                c='['+str(b)+']'
                shapes.append(c)
            else:
                shapes.append('null')
        return shapes
    except:
        return '边界获取失败'

#获取POI数量
def getnum(url):
    try:
        r = requests.get(url,'html.parser')
        mes = r.text
        count = re.findall('"count":"(.*?)"',mes)[0]
        return count
    except:
        return 'GETNUM ERROR'


#获取POI信息
def getmes(url,num,code,proxies):
    try:
        outfile = 'D://景点4.csv'
        f = open(outfile, 'a', newline='')
        writer = csv.writer(f)
        r = requests.get(url,'html.parser')
        mes = r.text
        type = []
        name = []
        ID = []
        location = []
        pname = []
        cityname = []
        adname = []
        type.extend(re.findall('"type":"(.*?)"',mes))
        ID.extend(re.findall('"id":"(.*?)"',mes))
        name.extend(re.findall('"name":"(.*?)",', mes))
        location.extend(re.findall('"location":"(.*?)",', mes))
        pname.extend(re.findall('"pname":"(.*?)",', mes))
        cityname.extend(re.findall('"cityname":"(.*?)",', mes))
        adname.extend(re.findall('"adname":"(.*?)",', mes))
        edge=getedge(ID,proxies)
        for i in range(len(type)):
            writer.writerow([name[i],ID[i],location[i],edge[i],pname[i],cityname[i],adname[i],type[i]])
        print("adcode="+str(code)+'第'+str(num)+"页已经爬取完毕，共有"+str(len(type))+"条数据")
    except:
        return 'GETMES ERROR'


if __name__ == '__main__':
    print("*************正在获取IP池**************")
    proxies = []
    proxies = get.main_function()
    print("*************IP池获取完毕**************")
    start=time.time()
    outfile = 'D://景点4.csv'
    f = open(outfile, 'a', newline='')
    writer = csv.writer(f)
    writer.writerow(["地点名", "地点ID", "经纬度", "边界","省份", "城市", "区县", "类型"])
    f.close()
    adcode=['110101']
    # ,'110102','110105','110106','110107','110108','110109','110111','110112','110113','110114','110115','110116','110117']
    pool = Pool(processes=2)
    for code in adcode:
        url='https://restapi.amap.com/v3/place/text?key=70cfe8605882530d550644f927ab4257&keywords=景点&city='+str(code)+'&citylimit=true&offset=20'
        mes=getnum(url)
        num = int(mes) / 20
        for i in range(1,int(num)+1):
            finurl = url + '&page=' + str(i)
            pool.apply_async(getmes, args=(finurl,i,code,proxies))
            # getmes(finurl,i,code,proxies)
    pool.close()
    pool.join()
    end=time.time()
    print('程序运行时间为'+str(end-start)+'seconds')





