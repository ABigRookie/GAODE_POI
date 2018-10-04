#本文件进行高德地图的大学POI信息获取并存入mongoDB数据库
import requests
import re
import csv
from multiprocessing import Pool
import time
import pymongo

#连接数据库
connection = pymongo.MongoClient()
POI = connection.POI
school = POI.school

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
def getmes(url):
    try:
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
        for i in range(len(type)):
            list = {}
            list['type'] = str(type[i])
            list['ID'] = str(ID[i])
            list['name'] = str(name[i])
            list['location'] = str(location[i])
            list['pname'] = str(pname[i])
            list['cityname']=str(cityname[i])
            list['adname']=str(adname[i])
            school.insert(list)
        print('此页共有'+str(len(type))+'条数据')
    except:
        return 'GETMES ERROR'

#global outfile

if __name__ == '__main__':
    start=time.time()
    keywords ='141201'
    adcode=['110101','110102','110105','110106','110107','110108','110109','110111','110112','110113','110114','110115','110116','110117']
    #pool = Pool(processes=2)
    for code in adcode:
        url='https://restapi.amap.com/v3/place/text?key=70cfe8605882530d550644f927ab4257&types='+str(keywords)+'&city=' +str(code) +'&citylimit=true&offset=20&children=1'
        mes=getnum(url)
        num = int(mes) / 20
        for i in range(1,int(num)+2):
            print("开始爬取 adcode=" + str(code) + '第' + str(i) + '页')
            finurl = url + '&page=' + str(i)
            #pool.apply_async(getmes, args=(finurl,i,code))
            getmes(finurl)
    # pool.close()
    # pool.join()
    end=time.time()
    print('程序运行时间为'+str(end-start)+'seconds')





