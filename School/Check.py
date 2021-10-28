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
