#通过获取该POI的具体信息，过滤掉无用POI
#其中，school表为可变量，可用其他数据表代替，其他代码无须改动
import pymongo
import requests
import re
import time

#连接数据库
connection = pymongo.MongoClient()
POI = connection.POI
school = POI.school

#获取网页内容
def gethtml(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text
    except:
        return '页面获取失败'

#获取边界
def getedge(ID):
    try:
        print(ID)
        url = 'https://www.amap.com/detail/get/detail?id='+str(ID)
        header = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36",
        }
        cookie = {
            "guid":"8fad-e1ec-039c-7162",
            "UM_distinctid":"164f3323b4e31-0fe089552c94db-f373567-1fa400-164f3323b4f1af",
            "cna":"ggNqEjFUsjoCAXaQhSTRVSfa",
            "_uab_collina":"153370435036652277261537",
            "passport_login":"MjA4NzEyNzQ3LGFtYXBfMTU4MDE2MjY4MzZBaTBEZ29rNTUsMXNiZG5qbGNvdW1scjc2M21ya3lva2hvNnk1M2s0MGcsMTUzNjgyMzc1OSxObU5qTkdVeU1HSXdNMkl4TW1JME9XRm1ZalE1TWpRNU5Ua3hOREF5TldFPQ%3D%3D",
            "dev_help":"YV9Qbf82jcWu45o2tPpMyzFkMGNkMzE5OGVjNjk2NDY2Y2E2YjI0ZjVjNWMxYjFmZWZhMGNkOWM0ODNkMjM0MmE3OGFhNjY4MGZiOGNlMGZTzTTKPHtP%2B4fkmBhgc4szKjmGAo6IJZ8EG5TDFgO2KgdbTj6znJseO%2BGGIJA6bTxg9onpn5O7dSJsFDGRYG2djTtWDk2HdqyqkwsfbyE%2FDibdnbm9AvHqQuVEr6sd61FSXcTpe142HiLWxyNr%2BvHM",
            "key":"bfe31f4e0fb231d29e1d3ce951e2c780",
            "CNZZDATA1255626299":"214960262-1533700612-https%253A%252F%252Fwww.baidu.com%252F%7C1538028684",
            "umdata":"C234BF9D3AFA6FE7B49D4CB1BB921D9EB1C17E5BA0E1264E4F0AFFC6D2C77E10B97D55CC695CE41CCD43AD3E795C914C0D3F214E05A24E06C243EB8602E9139A",
            "x5sec":"7b22617365727665723b32223a223335313963653561316163363930363331613232333364613635306265333438435076777364304645502f6672387232714b6e4163413d3d227d",
            "isg":"BPHxtciLDiwACaL-Oyu_Da47AH0nxdqL4XimvtMHcbjT-hdMDS0uIexcGM45Nv2I",
        }
        r = requests.get(url,headers=header,cookies=cookie)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        mes = r.text
        print(mes)
        area=re.findall('"area":"(.*?)",',mes)[0]
        print(area)
        school.update({"ID": id}, {"$set": {"area": area}})
        print("完成了ID:"+str(id)+"的面积获取")
        # shape=re.findall('"shape":"(.*?)",',mes)
        # if shape:
        #     shapes = {}
        #     b = shape[0].replace(';', '],[')
        #     c='['+str(b)+']'
        #     school.update({"ID":id}, {"$set": {"shape":c}})
        #     print("完成了ID:"+str(id)+"的边界获取")
        # else:
        #     school.remove({"ID":id})
        #     print("完成了ID:"+str(id)+"数据的删除")
    except:
        return '边界获取失败'

if __name__ == '__main__':
    for item in school.find():
        getedge(item['ID'])
        time.sleep(4)